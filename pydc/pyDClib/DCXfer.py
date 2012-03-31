# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import socket
import time
import DCWorker
from threading import Lock
from AsyncSocket import AsyncSocket
from DCChallenge import *
from Job import *

class DCXfer(object, Job):
	TYPE_UNKNOWN = 0
	TYPE_DOWNLOAD = 1
	TYPE_UPLOAD = 2

	STATUS_STOPPING = 100
	HANDSHAKE_TIMEOUT = 60

	def __init__(self, sock, listening = 1):
		self._type = self.TYPE_UNKNOWN
		self._remoteNick = None
		self._speed = SpeedStat()
		self.listening = listening
		self.reset()

		self.sock = sock
		self.lock = Lock()
		self.status = 0

	def copy(self, xfer):
		self._type = xfer._type
		self._remoteNick = xfer._remoteNick
		self._item = xfer._item
		self._sizeRemaining = xfer._sizeRemaining
		self._speed = xfer._speed
		self.timer = xfer.timer
		self.sock = xfer.sock
		self.lock = xfer.lock
		self.status = xfer.status

	def poll(self):
		if self.status == 0:
			try:
				self.sock.poll()
				if self.sock.isConnected():
					self.sendCmd("MyNick", DCWorker.getWorker().getUser().nick)
					self.sendCmd("Lock", "N*o=@:Tl,valyp=6d3weUQbDBV\U,W(9^?fb.dsqEn);3&7+, Pk=%@h0(oH]Nk(UZ)XE")
					self.setStatus(1)
			except socket.error:
				self.setStatus(self.STATUS_STOPPING)
				return 0

		elif self.status == 1:
			if time.time() - self.timer > self.HANDSHAKE_TIMEOUT:
				self.setStatus(self.STATUS_STOPPING)
				return 0

			try:
				self.sock.poll()
				if not self.sock.connected: raise socket.error
			except socket.error:
				self.setStatus(self.STATUS_STOPPING)
				return 0

			data = self.sock.recv()
			cmds = data.split("|")
			if self._remoteNick == None and len(cmds) > 0 and len(cmds[0]) > 0 and cmds[0][0] != '$':
				del cmds[0]
			
			for i in cmds:
				if len(i) > 0:
					if not self.parseHandshakeCmd(i):
						self.setStatus(self.STATUS_STOPPING)
						return 0

		elif self.status == DCXfer.STATUS_STOPPING:
			try:
				self.sock.close()
				if not self.sock.poll(): return 0
			except socket.error: pass

			self.status = DCXfer.STATUS_STOPPING + 1

			return 1

		else:
			return 1

		return 0

	def stop(self):
		self.setStatus(self.STATUS_STOPPING)

	def isAlive(self):
		return self.status < self.STATUS_STOPPING

	def getType(self):
		return self._type

	def getRemoteNick(self):
		return self._remoteNick

	def getItem(self):
		return self._item

	def getSize(self):
		if self._item != None:
			return self._item.size
		else:
			return 0L

	def getSizeRemaining(self):
		return self._sizeRemaining

	def getProgress(self):
		return 0

	def getSpeed(self):
		return self._speed.getSpeed()
		
	def getMinSpeed(self):
		return self._speed.getMinSpeed()
		
	def setMinSpeed(self, speed):
		self._speed.setMinSpeed(speed)

	#####################
	#  Private members  #
	#####################

	def reset(self):
		self._item = None
		self._sizeRemaining = 0L
		self._speed.reset()
		self.timer = time.time()

	def setStatus(self, status):
		self.lock.acquire()
		if status > self.status:
			self.status = status
		self.lock.release()

	def parseHandshakeCmd(self, cmd):
		if cmd[0] != "$": return 0

		cmd = cmd[1:]
		try:
			pos = cmd.index(" ")
			cmdname = cmd[:pos]
		except ValueError:
			return 0

		if cmdname == "MyNick":
			self._remoteNick = cmd[pos+1:]

		elif cmdname == "Lock":
			if self._remoteNick == None: return 0

			key = solveChallenge(cmd[pos+1:])
			if len(key) == 0: return 0

			item, source = DCWorker.getWorker().getQueue().getItemByNick(self._remoteNick)
			if item == None:
				self.sendCmd("Direction", "Upload", "30000")
				self._type = DCXfer.TYPE_UPLOAD
			else:
				self.sendCmd("Direction", "Download", "30000")
				self._type = DCXfer.TYPE_DOWNLOAD
			self.sendCmd("Key", key)

		elif cmdname == "Key":
			pass

		elif cmdname == "Direction":
			try: direction = cmd[pos+1:cmd.rindex(' ')]
			except ValueError: return 0

			if self.type == DCXfer.TYPE_DOWNLOAD:
				if direction != "Upload": return 0
			else:
				if direction != "Download": return 0

			x = DCWorker.getWorker().getXferListener()
			if self.type == DCXfer.TYPE_DOWNLOAD:
				x.createDownload(self)
			else:
				x.createUpload(self)

			self.setStatus(DCXfer.STATUS_STOPPING+1)
			return 0

		elif cmdname == "Capabilities":
			#DCTC specific command; ignore it
			return 1

		else:
			return 0

		return 1

	def sendCmd(self, cmd, *args):
		cmdstr = "$" + cmd
		for i in args:
			cmdstr += " " + i
		cmdstr += "|"

		self.sock.send(cmdstr)

	type = property(getType, None, None, None)
	remoteNick = property(getRemoteNick, None, None, None)
	item = property(getItem, None, None, None)
	size = property(getSize, None, None, None)
	sizeRemaining = property(getSizeRemaining, None, None, None)
	speed = property(getSpeed, None, None, None)
	minSpeed = property(getMinSpeed, setMinSpeed, None, None)

class SpeedStat:
	SPEED_RECORDS = 30
	MINSPEED_TIMEOUT = 30

	def __init__(self):
		self.reset()
		self.minSpeed = 1.0

	def reset(self):
		self.records = []
		self.minSpeedCount = 0
		self.time = 0

	def addRecord(self, curtime, l):
		speed = l / (curtime - self.time)

		self.records.append(speed)
		if len(self.records) > self.SPEED_RECORDS:
			self.records = self.records[-self.SPEED_RECORDS:]

		if self.time != 0:
			if speed < self.minSpeed:
				self.minSpeedCount += curtime - self.time
			else:
				self.minSpeedCount = 0

		self.time = curtime

	def getSpeed(self):
		if len(self.records) == 0: return 0
		acc = 0
		for i in self.records: acc += i
		return acc / len(self.records)

	def isSlow(self):
		return self.minSpeedCount >= self.MINSPEED_TIMEOUT

	def getLastTimestamp(self):
		return self.time

	def setMinSpeed(self, speed):
		self.minSpeed = speed
		self.minSpeedCount = self.MINSPEED_COUNTDOWN

	def getMinSpeed(self):
		return self.minSpeed
