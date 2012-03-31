# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os
import sys
import socket
import time
import DCWorker
from AsyncSocket import AsyncSocket
from DCQueueItem import *
from DCXfer import DCXfer


class DCDownload(DCXfer):
	SPEEDSTAT_TIMEOUT = 3
	ROLLBACK = 4096

	def __init__(self, xfer):
		DCXfer.copy(self, xfer)
		self._type = DCXfer.TYPE_DOWNLOAD

		self.file = None
		self.rollbackCounter = 0
		self.notified = 0

	def poll(self):
		if self.status == 1:
			self._item, source = DCWorker.getWorker().getQueue().getItemByNick(self._remoteNick)
			if self._item == None or self._item.status != DCQueueItem.STATUS_WAITING:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			try:
				file = open(self._item.getPath(), "rb")
				file.seek(0, 2)
				restart = file.tell()
				file.close()
			except IOError:
				restart = 0

			if self._item.size == restart:
				self._item.setStatusCompleted(self)
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			self.rollbackCounter = min(self.ROLLBACK, restart)
			restart -= self.rollbackCounter
			self.sendCmd("Get", source.path + "$" + str(restart+1))

			self._sizeRemaining = self._item.size - restart
			self.timer = time.time()
			self.setStatus(2)

		elif self.status == 2:
			if time.time() - self.timer > self.HANDSHAKE_TIMEOUT:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			try:
				self.sock.poll()
				if not self.sock.connected: raise socket.error
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

		elif self.status == 3:
			if self.rollbackCounter <= 0:
				self.setStatus(4)
				return 0
		
			try:
				self.sock.poll()
				if not self.sock.connected: raise socket.error
			except socket.error:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0
				
			newData = self.sock.recv(self.rollbackCounter)
			oldData = self.file.read(len(newData))
			l = len(newData)

			if l != len(oldData):
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0
			elif cmp(newData, oldData) != 0:
				self._item.removeSource(self._remoteNick)
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0
			
			self.rollbackCounter -= l
			self._sizeRemaining -= l
			self._item.setProgress((1 - (self._sizeRemaining * 1.0) / self._item.size) * 100)
		
		elif self.status == 4:
			try:
				self.sock.poll()
				if not self.sock.connected: raise socket.error
			except socket.error:
				self.setStatus(DCXfer.STATUS_STOPPING)
				return 0

			data = self.sock.recv()
			self._sizeRemaining -= len(data)
			self.file.write(data)
			curtime = time.time()
			self._speed.addRecord(curtime, len(data))

			if curtime - self.timer > self.SPEEDSTAT_TIMEOUT:
				self._item.setProgress((1 - (self._sizeRemaining * 1.0) / self._item.size) * 100)

				if self._speed.isSlow():
					self.setStatus(DCXfer.STATUS_STOPPING)
					return 0

				self.timer = curtime
				DCWorker.getWorker().getXferListener().onXferUpdate(self)

			if self._sizeRemaining <= 0:
				self.file = None
				self._item.setStatusCompleted(self)

				DCWorker.getWorker().getXferListener().onXferClosed(self)
				self.reset()
				self.notified = 0

				self.lock.acquire()
				if self.status < DCXfer.STATUS_STOPPING:
					self.status = 1
				self.lock.release()

		elif self.status == DCXfer.STATUS_STOPPING:
			self.sock.close()
			self.file = None

			if self._item != None:
				self._item.setStatusWaiting(self)

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
		if self._item != None:
			return self._item.progress
		else:
			return 0

	#####################
	#  Private methods  #
	#####################

	def basename(self, path):
		return path[path.rfind('\\')+1:]

	def parseCmd(self, cmd):
		if cmd[0] != "$": return 0

		cmd = cmd[1:]
		try:
			pos = cmd.index(" ")
			cmdname = cmd[:pos]
		except ValueError:
			#MaxedOut
			return 0

		if cmdname == "FileLength":
			if not self._item.setStatusRunning(self): return 0

			try:
				size = long(cmd[pos+1:])
				if self._item.size == -1L:
					self._item.setSize(size)
					self._sizeRemaining = size
				elif size != self._item.size:
					self._item.removeSource(self._remoteNick)
					raise ValueError()
			except ValueError:
				return 0

			self.sendCmd("Send")

			try:
				self.file = open(self._item.getPath(), "a+b")
				self.file.seek(-self.rollbackCounter, 2)

				if self._sizeRemaining != self._item.size - self.file.tell():
					raise IOError()
			except IOError:
				return 0

			self.setStatus(3)
			self.notified = 1
			DCWorker.getWorker().getXferListener().onNewXfer(self)

		elif cmdname == "Error":
			self._item.removeSource(self._remoteNick)
			return 0

		else:
			return 0

		return 1
		
	progress = property(getProgress, None, None, None)
