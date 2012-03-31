# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import errno
import os
import struct
import sys
import time
from socket import *
from threading import Lock
from Job import *

class DNS:
	def __init__(self):
		self.servers = []
		self.serial = 0

		if os.name == "posix":
			try:
				f = open("/etc/resolv.conf")
				lines = f.readlines()
				f.close()
			except IOError:
				raise NoDNSServer()

			for line in lines:
				if line[:11] == "nameserver ":
					self.servers.append(line[11:-1].strip())

		elif os.name == "nt":
			import win32dns

			self.servers = win32dns.RegistryResolve()
			if len(self.servers) == 0:
				raise NoDNSServer()

	def getSerial(self):
		serial = self.serial
		self.serial += 1
		if self.serial > 0xffff: self.serial = 0
		return serial

class DNSResolver(Job):
	def __init__(self, addr, timeout = 10):
		self.serial = 0
		self.addr = addr
		self.resolved = None
		self.sock = None
		self.lock = Lock()

		self.questionLen = 0
		self.reply = None
		self.replyPos = 0
		self.status = 0
		self.starttime = 0
		self.timeout = timeout

	def poll(self):
		if self.status == 0:
			request = self.buildRequest()

			self.sock = socket(AF_INET, SOCK_DGRAM)
			self.sock.setblocking(0)
			self.sock.connect((getDNS().servers[0], 53))
			self.sock.send(request)

			self.setStatus(1)
			self.starttime = time.time()

		elif self.status == 1:
			try:
				self.reply = self.sock.recv(1024)
			except error, e:
				if time.time() - self.starttime >= self.timeout:
					self.setStatus(2)
					raise DNSError, "timeout while waiting reply"

				if self.isWouldBlock(e[0]):
					return 0
				else:
					self.setStatus(2)
					raise DNSError, "broken connection with server"

			if self.parseReply():
				self.setStatus(2)
				if self.resolved == None:
					raise DNSError, "address unknown"
			else:
				self.lock.acquire()
				if self.status < 2:
					self.status = 0
				self.lock.release()

		elif self.status == 2:
			if self.sock != None:
				self.sock = None

			self.server = None
			self.reply = None
			self.setStatus(3)

			return 1

		else:
			return 1

		return 0

	def stop(self):
		self.setStatus(2)

	def isAlive(self):
		return self.status != 2

	#####################
	#  Private members  #
	#####################

	def setStatus(self, status):
		self.lock.acquire()
		if status > self.status:
			self.status = status
		self.lock.release()

	def isWouldBlock(self, code):
		if os.name == "posix":
			if code == errno.EAGAIN or code == errno.EALREADY or code == errno.EINPROGRESS:
				return 1
		elif os.name == "nt":
			if code == errno.WSAEWOULDBLOCK:
				return 1

		return 0

	def buildRequest(self):
		self.serial = getDNS().getSerial()
		self.questionLen = 0
		buf =  ""

		#Header
		buf += self.pack16bit(self.serial)
		buf += self.pack16bit(1<<8)
		buf += self.pack16bit(1)
		buf += self.pack16bit(0)
		buf += self.pack16bit(0)
		buf += self.pack16bit(0)

		#Question
		for label in self.addr.split('.'):
			llen = len(label)
			if llen > 63: raise DNSError, "label too long"
			buf += chr(llen) + label
			self.questionLen += llen + 1
		buf += '\0'
		buf += self.pack16bit(1)
		buf += self.pack16bit(1)
		self.questionLen += 5

		return buf

	def parseReply(self):
		self.replyPos = 0

		#Header
		if self.get16bit() != self.serial:
			raise DNSError, "unexpected ID"
		flags = self.get16bit()
		if (flags>>15)&1 != 1: raise DNSError, "reply error"
		if (flags>>0)&0xF != 0:
			if (flags>>0)&0xF == 3: return 1
			else: raise DNSError, "server failure"
		#print self.get16bit(), self.get16bit(), self.get16bit(), self.get16bit()
		question = self.get16bit()
		answer = self.get16bit()
		authority = self.get16bit()
		self.replyPos += 2

		if question == 1: self.replyPos += self.questionLen
		if answer == 0 and authority == 0: raise DNSError, "reply error"

		rrs = []
		for i in range(0, answer+authority):
			type, data = self.parseRR()
			if type == 1:
				self.resolved = data
				return 1
			else:
				rrs.append((type, data))

		addrs = filter(lambda i: i[0] == 2, rrs)
		if len(addrs) != 0:
			self.server = addrs[0][1]
			return 0

		return 1

	def parseRR(self):
		name = self.getname()
		type = self.get16bit()
		if self.get16bit() != 1: raise DNSError, "reply error"
		self.replyPos += 4
		rlen = self.get16bit()

		if type == 1:
			data = inet_ntoa(self.reply[self.replyPos:self.replyPos+4])
			self.replyPos += rlen
		elif type == 2:
			data = self.getname()
		elif type == 5:
			data = self.getname()
		else:
			raise DNSError, "reply error"

		return type, data

	def get8bit(self):
		bits = self.reply[self.replyPos]
		self.replyPos += 1
		return bits

	def get16bit(self):
		bits = self.reply[self.replyPos:self.replyPos+2]
		self.replyPos += 2
		return self.unpack16bit(bits)

	def getname(self):
		labels = []

		while 1:
			llen = ord(self.get8bit())

			if llen == 0: break
			elif llen & 0xC0 == 0xC0:
				j = ord(self.get8bit())
				pointer = ((llen<<8) | j) & ~0xC000

				realPos = self.replyPos
				self.replyPos = pointer
				labels.append(self.getname())
				self.replyPos = realPos

				break
			else:
				labels.append(self.reply[self.replyPos:self.replyPos+llen])
				self.replyPos += llen

		if len(labels) == 0: raise DNSError, "RR name is null"
		name = ""
		for i in range(0, len(labels)-1):
			name += labels[i] + '.'
		name += labels[-1]
		return name

	def pack16bit(self, n):
		return struct.pack('!H', n)

	def unpack16bit(self, s):
		return struct.unpack('!H', s)[0]

class NoDNSServer(Exception): pass
class DNSError(Exception): pass

#Global object
sys.modules["__main__"].dns = DNS()

def getDNS():
	return sys.modules["__main__"].dns

if __name__ == "__main__":
	r = DNSResolver(sys.argv[1])
	while not r.poll(): pass
	print "Resolved:", r.resolved
