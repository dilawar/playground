# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from Job import *
from DCSearchResult import *
from threading import Lock
from socket import *
from DCSearch import *
import DCWorker
from socket import *
import os
import errno
import time

class DCSearchWorker(object, EventGenerator, Job):
	SEARCH_INTERVAL = 10
	SEARCH_TIMEOUT = 300

	def __init__(self, address, port):
		EventGenerator.__init__(self)
	
		self.opLock = Lock()
		
		if port == 0:
			self.sock = None
		else:
			self.sock = socket(AF_INET, SOCK_DGRAM)
			self.sock.bind((address, port))
			self.sock.setblocking(0)

		self._searches = []
		self._queue = []
		self.results = []
		self.status = 0

	def poll(self):
		if self.status == 0:
			self.opLock.acquire()
			t = time.time()

			removed = []
			for i in self._searches:
				if t - i[1] >= self.SEARCH_TIMEOUT:
					removed.append(i[0])

			if len(self._queue) > 0:
				if len(self._searches) == 0 or t - self._searches[-1][1] > self.SEARCH_INTERVAL:
					search = self._queue.pop(0)
					self._searches.append([search, t])
					self.runSearch(search)

			self.opLock.release()
			for s in removed: s.stop()

			if self.sock != None:
				try:
					while 1:
						data, addr = self.sock.recvfrom(2048)

						if data[:3] == '$SR':
							result = self.parseResult(data[4:])
							if result != None:
								self.lock.acquire()
								for i in self._searches:
									i[0].onNewResult(result)
								self.lock.release()

				except error, e:
					if self.isWouldBlock(e[0]): pass
					else: pass #discard silently
					#raise e
				
			self.opLock.acquire()
			results = self.results
			self.results = []
			self.opLock.release()
			
			for result in results:
				res = self.parseResult(result)
				if res != None:
					self.lock.acquire()
					for i in self._searches:
						i[0].onNewResult(res)
					self.lock.release()

		elif self.status == 1:
			if self.sock != None:
				self.sock.close()

			self.opLock.acquire()
			self._searches = []
			self._queue = []
			self.opLock.release()

			self.status = 2
			return 1

		else:
			return 1

		return 0

	def stop(self):
		self.status = 1

	def isAlive(self):
		return self.status == 0
		
	def passiveResult(self, data):
		self.opLock.acquire()
		self.results.append(data)
		self.opLock.release()
		
	def sendResult(self, addr, data):
		if self.sock == None: return
		
		try: self.sock.sendto(data, addr)
		except error: pass

	def getSearches(self):
		self.opLock.acquire()
		searches = []
		for i in self._searches:
			searches.append(i[0])
		self.opLock.release()
		
		return searches

	def registerSearch(self, search, nodelay):
		self.opLock.acquire()
		curtime = time.time()
		start = 0

		if len(self._searches) != 0 and curtime - self._searches[-1][1] < self.SEARCH_INTERVAL:
			if nodelay:
				self.opLock.release()
				return 0
			else:
				self._queue.append(search)
		else:
			self._searches.append([search, curtime])
			start = 1
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			listener.onNewSearch(search)
		self.lock.release()

		if start: self.runSearch(search)
		return 1

	def deregisterSearch(self, search):
		self.opLock.acquire()

		aux = []
		for i in self._searches:
			if i[0] != search:
				aux.append(i)
		self._searches = aux

		try: self._queue.remove(search)
		except ValueError: pass

		self.opLock.release()

	def deregisterAllListeners(self):
		self.opLock.acquire()
		for search in self._searches:
			try: search.deregisterAllListeners()
			except AttributeError: pass
		self.opLock.release()

		EventGenerator.deregisterAllListeners(self)

	#=================#
	# Private section #
	#=================#

	def isWouldBlock(self, code):
		if os.name == "posix":
			if code == errno.EAGAIN or code == errno.EALREADY or code == errno.EINPROGRESS or code == errno.EINTR:
				return 1
		elif os.name == "nt":
			if code == errno.WSAEWOULDBLOCK:
				return 1

	def runSearch(self, search):
		worker = DCWorker.getWorker()
		for hub in worker.getHubs():
			hub.startSearch(search, worker.getSettings().active)

	def parseResult(self, data):
		#TODO: correctly parse directory results
		try:
			result = DCSearchResult()

			pos = data.index(' ')
			result.userNick = data[:pos]
			data = data[pos+1:]

			pos = data.index('\5')
			result.path = data[:pos]
			result.type = result.path[result.path.rfind('.')+1:]
			data = data[pos+1:]

			pos = data.index(' ')
			result.size = long(data[:pos])
			data = data[pos+1:]

			pos = data.index('/')
			result.freeSlots = int(data[:pos])
			data = data[pos+1:]

			pos = data.index('\5')
			result.slots = int(data[:pos])
			data = data[pos+1:]

			result.hubName = data[:data.rindex('(')-1]

			return result
		except ValueError:
			return None

	searches = property(getSearches, None, None, None)

