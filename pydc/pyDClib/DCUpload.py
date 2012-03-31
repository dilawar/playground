# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os
import os.path
import sys
import socket
import time
import DCWorker
from AsyncSocket import AsyncSocket
from DCItem import DCItem
from DCXfer import DCXfer

class DCUpload(DCXfer):
	SPEEDSTAT_TIMEOUT = 3

	def __init__(self, xfer):
		DCXfer.copy(self, xfer)
		self._type = DCXfer.TYPE_UPLOAD

		self._progress = 0
		self.file = None
		self.notified = 0
		self.acquiredSlot = 0

	def poll(self):
		if self.status == 1:
			if time.time() - self.timer > self.HANDSHAKE_TIMEOUT:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			try:
				self.sock.poll()
				if not self.sock.isConnected(): raise socket.error
			except socket.error, e:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			data = self.sock.recv()
			cmds = data.split("|")
			for i in cmds:
				if len(i) > 0:
					if not self.parseCmd(i):
						self.setStatus(DCXfer.STATUS_STOPPING)
						return 0

		elif self.status == 2:
			xferListener = DCWorker.getWorker().getXferListener()
			bps = xferListener.getUploadBps()
			curtime = time.time()

			if bps:
				delta = self._speed.getLastTimestamp()
				if delta == 0:
					delta, bytes = 1, int(bps)
				else:
					delta = curtime - delta
					bytes = int(delta * bps - self.sock.getBytesToSend())

				if bytes > 0:
					try:
						self.sock.send(self.file.read(bytes))
						self._sizeRemaining -= bytes
					except IOError:
						self.setStatus(DCXfer.STATUS_STOPPING)
						return 0
					except MemoryError:
						self.setStatus(DCXfer.STATUS_STOPPING)
						return 0
			else:
				try:
					if self.sock.getBytesToSend() <= 1000:
						data = self.file.read(65536)
						self.sock.send(data)
						self._sizeRemaining -= len(data)
				except IOError:
					self.setStatus(DCXfer.STATUS_STOPPING)
					return 0

			try:
				bytes = self.sock.getBytesToSend()
				self.sock.poll()
				if not self.sock.isConnected(): raise socket.error
			except socket.error:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			bytes -= self.sock.getBytesToSend()
			if bps: xferListener.setUnusedUploadBps(bps - (float(bytes) / delta))
			self._speed.addRecord(curtime, bytes)

			if curtime - self.timer > self.SPEEDSTAT_TIMEOUT:
				self._progress = (1 - (self._sizeRemaining * 1.0) / self._item.size) * 100

				if self._speed.isSlow():
					self.setStatus(DCXfer.STATUS_STOPPING)
					return 0

				self.timer = curtime
				xferListener.onXferUpdate(self)

			if self._sizeRemaining <= 0:
				self.file = None

				xferListener.onXferClosed(self)
				if self.acquiredSlot:
					DCWorker.getWorker().releaseSlot()

				self.reset()
				self._progress = 0
				self.notified = 0
				self.acquiredSlot = 0

				self.lock.acquire()
				if self.status < DCXfer.STATUS_STOPPING:
					self.status = 1
				self.lock.release()

		elif self.status == DCXfer.STATUS_STOPPING:
			try:
				self.sock.close()
				if not self.sock.poll(): return 0
			except socket.error: pass

			self.file = None
			if self.acquiredSlot:
				DCWorker.getWorker().releaseSlot()

			self.status = DCXfer.STATUS_STOPPING + 1
			if self.notified: DCWorker.getWorker().getXferListener().onXferClosed(self)

			return 1

		else:
			return 1

		return 0

	def stop(self):
		self.setStatus(DCXfer.STATUS_STOPPING)

	def isAlive(self):
		return self.status < DCXfer.STATUS_STOPPING

	def getProgress(self):
		return self._progress

	#####################
	#  Private methods  #
	#####################

	def reset(self):
		self._item = None
		DCXfer.reset(self)

	def basename(self, path):
		return path[path.rindex('\\')+1:]

	def parseCmd(self, cmd):
		if cmd[0] != "$": return 0

		cmd = cmd[1:]
		try:
			pos = cmd.index(" ")
			cmdname = cmd[:pos]
		except ValueError:
			if cmd == "GetListLen":
				try:
					file = open("MyList.DcLst", 'rb')
					file.seek(0, 2)
					size = str(file.tell())
					file.close()

					self.sendCmd("ListLen", size)
				except IOError:
					self.sendCmd("Error")
					return 0

			elif cmd == "Send":
				if self._item == None:
					self.sendCmd("Error")
					return 0

				self.setStatus(2)
				self.notified = 1
				DCWorker.getWorker().getXferListener().onNewXfer(self)

			else:
				self.sendCmd("Error")
				return 0

			return 1

		if cmdname == "Get":
			info = cmd[pos+1:].split('$')
			if len(info) != 2:
				return 0

			try: info[1] = max(long(info[1])-1, 0)
			except ValueError:
				self.sendCmd("Error")
				return 0

			try:
				if info[0] == "MyList.DcLst":
					file = "MyList.DcLst"
					self.file = open(file, 'rb')
				else:
					if DCWorker.getWorker().acquireSlot():
						self.acquiredSlot = 1
					else:
						raise IOError

					idx = info[0].find('\\')
					if idx == -1: raise IOError
					base = info[0][:idx]

					for p in DCWorker.getWorker().getSettings().share:
						if os.path.basename(p) != base:
							continue

						file = p + os.sep + info[0][idx+1:].replace('\\', os.sep)
						try:
							self.file = open(file, 'rb')
							break
						except IOError:
							pass

					if self.file == None: raise IOError

				self._item = DCItem()
				self._item.userNick = DCWorker.getWorker().getUser().nick
				self._item.path = file

				self.file.seek(0, 2)
				self._item.size = self.file.tell()
				self.file.seek(info[1], 0)
				self._sizeRemaining = self._item.size - self.file.tell()

			except IOError:
				self.sendCmd("Error")
				return 0

			self.sendCmd("FileLength", str(self._item.size))

		else:
			return 0

		return 1

	progress = property(getProgress, None, None, None)
