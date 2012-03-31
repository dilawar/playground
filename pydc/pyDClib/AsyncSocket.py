# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os
import errno
import time
from socket import *
from threading import Lock
from DNS import *

class AsyncSocket(object, Job):
	STATUS_READY = 0
	STATUS_RESOLVING = 1
	STATUS_CONNECTING = 2
	STATUS_CONNECTED = 3
	STATUS_CLOSING = 4
	STATUS_CLOSED = 5

	CONNECTION_TIMEOUT = 30

	def __init__(self, sock = None):
		self.resolver = None
		self.lock = Lock()
		self.host = None
		self._status = self.STATUS_READY
		self.error = None
		self.timer = 0

		if sock:
			self.setSocket(sock)
		else:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.setblocking(0)

		self.inbuf = ""
		self.outbuf = ""

	def setSocket(self, sock):
		if self._status != self.STATUS_READY:
			raise error, (errno.EBADF, "Socket not ready")

		self.sock = sock
		if not self.isConnected():
			self._status = self.STATUS_CLOSED
			raise error, (errno.EBADF, "Invalid socket")

		self.sock.setblocking(0)
		self._status = self.STATUS_CONNECTED

	def connect(self, host):
		if self._status != self.STATUS_READY:
			raise error, (errno.EBADF, "Socket not ready")

		self.host = host
		self.timer = time.time()

		try:
			inet_aton(host[0])
			self.setStatus(self.STATUS_CONNECTING)
		except:
			self.setStatus(self.STATUS_RESOLVING)
			self.resolver = DNSResolver(host[0])

	def close(self):
		self.setStatus(self.STATUS_CLOSING)

	def poll(self):
		if self._status == self.STATUS_READY:
			raise error, (errno.ENOTCONN, "Socket not connected")

		elif self._status == self.STATUS_RESOLVING:
			try:
				if self.resolver.poll():
					self.host = (self.resolver.resolved, self.host[1])
					self.resolver = None
					self.setStatus(self.STATUS_CONNECTING)
					self.timer = time.time()
			except DNSError:
				self.error = error(errno.EADDRNOTAVAIL, "DNS error")
				self.setStatus(self.STATUS_CLOSING)
				return 0

		elif self._status == self.STATUS_CONNECTING:
			if time.time() - self.timer > self.CONNECTION_TIMEOUT:
				self.error = error(errno.ETIMEDOUT, "Timeout while connecting")
				self.setStatus(self.STATUS_CLOSING)
				return 0

			try:
				self.sock.connect(self.host)
				self.setStatus(self.STATUS_CONNECTED)
				self.host = None
			except error, e:
				if self.isWouldBlock(e[0]): pass
				elif os.name == "nt":
					if e[0] == errno.WSAEISCONN:
						self.setStatus(self.STATUS_CONNECTED)
						self.host = None
					elif e[0] == errno.WSAEINVAL:
						pass
					else:
						self.error = e
						self.setStatus(self.STATUS_CLOSING)
						return 0
				else:
					self.error = e
					self.setStatus(self.STATUS_CLOSING)
					return 0

		elif self._status == self.STATUS_CONNECTED:
			try:
				data = self.sock.recv(65536)
				if len(data) == 0:
					self.setStatus(self.STATUS_CLOSING)
					return 0
				else:
					self.lock.acquire()
					self.inbuf += data
					self.lock.release()
			except error, e:
				if self.isWouldBlock(e[0]): pass
				else:
					self.error = e
					self.setStatus(self.STATUS_CLOSING)
					return 0
					
			if len(self.outbuf) > 0:
				try:
					sent = self.sock.send(self.outbuf)

					self.lock.acquire()
					self.outbuf = self.outbuf[sent:]
					self.lock.release()
				except error, e:
					if self.isWouldBlock(e[0]): pass
					else:
						self.error = e
						self.setStatus(self.STATUS_CLOSING)
						return 0

		elif self._status == self.STATUS_CLOSING:
			if self.resolver != None:
				self.resolver.stop()

				try:
					if self.resolver.poll():
						self.resolver = None
					else:
						return 0
				except DNSError:
					self.resolver = None

			self.sock = None
			self.lock.acquire()
			self.outbuf = ''
			self.lock.release()
			
			self.setStatus(self.STATUS_CLOSED)

			if self.error:
				raise self.error

			return 1

		else:
			return 1

		return 0

	def recv(self, size = -1):
		self.lock.acquire()
		if size == -1 or len(self.inbuf) < size:
			size = len(self.inbuf)
		if size == 0:
			self.lock.release()
			return ""

		data = self.inbuf[:size]
		self.inbuf = self.inbuf[size:]
		self.lock.release()

		return data

	def send(self, data):
		self.lock.acquire()
		self.outbuf += data
		self.lock.release()

	def getStatus(self):
		return self._status

	def getBytesToSend(self):
		return len(self.outbuf)

	def getpeername(self):
		try:
			name = self.sock.getpeername()
		except AttributeError:
			return None
		except error:
			return None

		return name

	def isAlive(self):
		self.lock.acquire()
		res = self._status > self.STATUS_READY and self._status <= self.STATUS_CLOSING
		self.lock.release()
		return res

	def isConnected(self):
		return self.getpeername() != None

	#=================#
	# Private section #
	#=================#

	def setStatus(self, status):
		self.lock.acquire()
		if status > self._status:
			self._status = status
		self.lock.release()

	def isWouldBlock(self, code):
		if os.name == "posix":
			if code == errno.EAGAIN or code == errno.EALREADY or code == errno.EINPROGRESS or errno.EINTR:
				return 1
		elif os.name == "nt":
			if code == errno.WSAEWOULDBLOCK:
				return 1

		return 0

	status = property(getStatus, None, None, None)
	bytesToSend = property(getBytesToSend, None, None, None)
	peername = property(getpeername, None, None, None)
	alive = property(isAlive, None, None, None)
	connected = property(isConnected, None, None, None)

