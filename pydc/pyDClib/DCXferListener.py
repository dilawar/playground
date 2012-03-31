# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from AsyncSocket import *
from EventGenerator import *
from Job import *
from DCQueue import *
import DCWorker
from DCXfer import DCXfer
from DCDownload import DCDownload
from DCUpload import DCUpload
from threading import Lock
from socket import *
from copy import copy
import os
import errno

class DCXferListener(object, Job, EventGenerator):
	def __init__(self, address, port):
		EventGenerator.__init__(self)

		if port == 0:
			self.sock = None
		else:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.bind((address, port))
			self.sock.listen(3)
			self.sock.setblocking(0)

		self._xfers = []
		self._uploadLimit = 0
		self.uploadBps = [0, 0]
		self.status = 0
		self.opLock = Lock()

	def poll(self):
		if self.status == 0:
			if self.sock != None:
				try:
					conn, addr = self.sock.accept()
					DCWorker.getWorker().addJob(DCXfer(AsyncSocket(conn)))
				except error: pass

		elif self.status == 1:
			if self.sock != None:
				self.sock.close()
				
			self.status = 2
			return 1

		else:
			return 1
	
		return 0

	def stop(self):
		self.status = 1

	def isAlive(self):
		return self.status == 0

	def getXfers(self):
		self.opLock.acquire()
		xfers = copy(self._xfers)
		self.opLock.release()

		return xfers
		
	def stopXfer(self, item, source=None):
		self.opLock.acquire()
		for xfer in self._xfers:
			if xfer.item == item:
				if source == None or xfer.remoteNick == source.nick:
					xfer.stop()
					break
		self.opLock.release()
		
	def createDownload(self, xfer):
		DCWorker.getWorker().addJob(DCDownload(xfer))
		
	def createUpload(self, xfer):
		DCWorker.getWorker().addJob(DCUpload(xfer))

	def setUploadLimit(self, bps):
		# TODO: check bps
		self._uploadLimit = bps
		self.setUploadBps()

	def getUploadLimit(self):
		return self._uploadLimit

	def getUploadBps(self):
		if self._uploadLimit == 0: return 0

		self.opLock.acquire()
		bps = min(self.uploadBps[0] + self.uploadBps[1], self._uploadLimit)
		self.opLock.release()
		return bps

	def setUnusedUploadBps(self, bps):
		self.uploadBps[1] = max(bps, 0)

	def onNewXfer(self, xfer):
		self.opLock.acquire()
		self._xfers.append(xfer)
		self.setUploadBps()
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			listener.onNewXfer(xfer)
		self.lock.release()

	def onXferUpdate(self, xfer):
		self.lock.acquire()
		for listener in self.listeners:
			listener.onXferUpdate(xfer)
		self.lock.release()

	def onXferClosed(self, xfer):
		self.opLock.acquire()
		self._xfers.remove(xfer)
		self.setUploadBps()
		self.opLock.release()
		
		self.lock.acquire()
		for listener in self.listeners:
			listener.onXferClosed(xfer)
		self.lock.release()

	#=================#
	# Private section #
	#=================#

	def setUploadBps(self):
		uploadNum = 0
		for xfer in self._xfers:
			if xfer.getType() == DCXfer.TYPE_UPLOAD:
				uploadNum += 1

		self.uploadBps[0] = max(float(self._uploadLimit) / max(uploadNum, 1), 1)

	def isWouldBlock(self, code):
		if os.name == "posix":
			if code == errno.EAGAIN or code == errno.EALREADY or code == errno.EINPROGRESS:
				return 1
		elif os.name == "nt":
			if code == errno.WSAEWOULDBLOCK:
				return 1
				
	xfers = property(getXfers, None, None, None)
	uploadLimit = property(getUploadLimit, setUploadLimit, None, None)
