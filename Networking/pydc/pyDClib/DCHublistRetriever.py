# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from socket import error
from urlparse import urlparse
import time

from AsyncSocket import *
from EventGenerator import *
from Job import *
import DCWorker

class DCHublistRetriever(object, Job, EventGenerator):
	LIST_TIMEOUT = 15

	def __init__(self, sources = None):
		EventGenerator.__init__(self)

		if sources == None:
			sources = DCWorker.getWorker().getSettings().hublists
		
		self.sources = []
		for addr in sources:
			i = urlparse(addr)
			if i[0] != 'http':
				raise IllegalProtocolError()
				
			pos = i[1].rfind(':')
			if pos != -1:
				try:
					host = (i[1][:pos], int(i[1][pos+1]))
				except ValueError:
					raise IllegalPortError()
			else:
				host = (i[1], 80)
			
			self.sources.append((host, i[2]))
		
		self.status = 0
		self._hubs = {}
		self.sock = None
		self.timestamp = 0

	def poll(self):
		try:
			if self.status == 0:
				if len(self.sources) == 0:
					self.status = 3
					
					self.lock.acquire()
					for listener in self.listeners:
						listener.onHublist(self._hubs.values())
					self.lock.release()
					
					return 1
			
				addr = self.sources[0]
				del self.sources[0]
			
				self.sock = AsyncSocket()
				self.sock.connect(addr[0])

				request =  'GET %s HTTP/1.0\r\n' % addr[1] 
				request += 'Host: %s\r\n\r\n' % addr[0][0]
				self.sock.send(request)
				self.sock.poll()

				self.timestamp = time.time()
				self.setStatus(1)

			elif self.status == 1:
				if time.time() - self.timestamp > DCHublistRetriever.LIST_TIMEOUT:
					self.setStatus(2)

				self.sock.poll()

				if not self.sock.isAlive():
					self.parse(self.sock.recv())
					self.setStatus(2)

			else:
				if self.sock != None:
					self.sock.close()
					if self.sock.poll():
						self.sock = None
						
						if self.status == 2:
							self.setStatus(0)
					else:
						return 0
				else:
					return 1

			return 0

		except error:
			self.setStatus(2)
			return 0

		except DNSError:
			self.setStatus(2)
			return 0

	def stop(self):
		self.lock.acquire()
		self.status = 3
		self.lock.release()
		
	def getHubs(self):
		return self._hubs.values()

	###################
	# Private methods #
	###################
                
	def setStatus(self, code):
		self.lock.acquire()
		if self.status < 3:
			self.status = code
		self.lock.release()
	
	def parse(self, data):
		i, datalen = 0, len(data)
		start, col = 0, 0
		hub = ["", "", "", 0]

		#Skip HTTP header
		while i < datalen:
			if data[i:i+4] == '\r\n\r\n': break
			i += 1
		if i >= datalen:
			return 0
		i += 4
		start = i

		while i < datalen:
			if data[i] == "|":
				hub[col] = data[start:i]
				col += 1
				if col > 3:
					try:
						hub[3] = int(hub[3])
						self._hubs[hub[1]] = hub
					except ValueError: pass
										
					hub = ["", "", "", 0]
					i += 6
					col = 0
				start = i+1

			i += 1

		return 1
		
	hubs = property(getHubs, None, None, None)
	
class IllegalProtocolError(Exception): pass
class IllegalPortError(Exception): pass
