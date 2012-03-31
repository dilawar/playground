# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from EventGenerator import *
from DCSettings import DCSettings
from DCLocalIP import *
from DCSearchWorker import *
from DCXferListener import *
from DCQueue import *
from DCHub import *
from DCLocalList import *
from DCLocalListWriter import *
from thread import start_new_thread
from threading import Lock
import atexit
import socket
import sys
import time

class DCWorker(object, EventGenerator):
	CLOSING_COUNTDOWN = 10

	def __init__(self):
		EventGenerator.__init__(self)
	
		self._settings = None
		self.opLock = Lock()

		self.running = 0
		self.sleepTime = 0.2
		self._jobs = []
		self.addedJobs = {}
		self.removedJobs = {}

		self._localAddress = None
		self._searchWorker = None
		self._xferListener = None
		self._queue = None
		self._localLists = []
		self._usedSlots = 0

		atexit.register(self.stop)

	def getSettings(self):
		if self._settings == None: raise SettingsException()
		return self._settings

	def getUser(self):
		if self._settings == None: raise SettingsException()
		return self._settings.user

	def getLocalAddress(self):
		if self._settings == None: raise SettingsException()
		return self._localAddress

	def getSearchWorker(self):
		return self._searchWorker

	def getXferListener(self):
		return self._xferListener

	def getQueue(self):
		return self._queue
	
	def getLocalLists(self):
		#update = 0
		#for i in self._localLists:
		#	if i.scan(): update = 1

		#if update:
		#	acc = 0L
		#	for l in self._localLists:
		#		acc += l.getSize()

		#	self._settings.user.share = acc
		#	DCLocalListWriter().write("MyList.DcLst", self._localLists)

		return self._localLists
		
	def getUsedSlots(self):
		self.opLock.acquire()
		slots = self._usedSlots
		self.opLock.release()
		return slots
		
	def getJobs(self):
		self.opLock.acquire()
		jobs = copy(self._jobs)
		self.opLock.release()

		return jobs
		
	def getXfers(self):
		return self._xferListener.getXfers()

	def getHubs(self):
		self.opLock.acquire()
		hubs = []
		for job in self._jobs:
			if isinstance(job, DCHub) and job.isAlive():
				hubs.append(job)
		self.opLock.release()

		return hubs

	def getHubByName(self, name):
		self.opLock.acquire()
		hub = None
		for job in self._jobs:
			if isinstace(job, DCHub) and job.name == name and job.isAlive():
				hub = job
				break
		self.opLock.release()

		return hub

	def getUsersByNick(self, nick):
		self.opLock.acquire()

		users = []
		for job in self._jobs:
			if isinstance(job, DCHub) and job.isAlive():
				user = job.getUserByNick(nick)
				if user != None: users.append(user)

		self.opLock.release()
		return users

	def start(self):
		if self._settings == None:
			raise SettingsException()

		start_new_thread(self.run, ())

	def stop(self):
		if self.running == 0:
			return
		elif self.running > 0:
			self.running = -1

		if self.running < 0:
			while self.running != -2:
				time.sleep(self.sleepTime)

			try:
				if self._queue:
					self._queue.save()
			except IOError: pass

			try: os.unlink('MyList.DcLst')
			except OSError: pass

	def run(self):
		closingJobs = []
		self.running = 1

		while self.running > 0:
			newJobs = []
			for i in self._jobs:
				if not i.poll():
					newJobs.append(i)

			aux = []
			for i in closingJobs:
				if not i[0].poll():
					i[1] -= 1
					if i[1] > 0:
						aux.append([i[0], i[1]])
			closingJobs = aux

			self._searchWorker.poll()
			self._xferListener.poll()
			self._queue.poll()

			self.opLock.acquire()

			iter = self.removedJobs.iterkeys()
			try:
				while 1:
					job = iter.next()

					if self.addedJobs.has_key(job):
						del self.addedJobs[job]
					elif job in newJobs:
						newJobs.remove(job)
						job.stop()
						closingJobs.append([job, self.CLOSING_COUNTDOWN])

			except StopIteration:
				self.removedJobs = {}

			iter = self.addedJobs.iterkeys()
			aux = {}
			connecting = 0
			try:
				while 1:
					job = iter.next()

					if job.__class__ == DCHub:
						if job.status == DCHub.STATUS_CONNECTING:
							if connecting == 0:
								newJobs.append(job)
								connecting = 1
							else:
								aux[job] = 1
						else:
							newJobs.append(job)
					else:
						newJobs.append(job)

			except StopIteration:
				self.addedJobs = aux

			self._jobs = newJobs

			self.opLock.release()
			time.sleep(self.sleepTime)

		#Stop all jobs
		for i in self._jobs:
			i.stop()
		self._searchWorker.stop()
		self._xferListener.stop()
		self._queue.stop()

		for i in self._jobs:
			closingJobs.append([i, self.CLOSING_COUNTDOWN])
		closingJobs.append([self._searchWorker, self.CLOSING_COUNTDOWN])
		closingJobs.append([self._xferListener, self.CLOSING_COUNTDOWN])
		closingJobs.append([self._queue, self.CLOSING_COUNTDOWN])
		
		self.opLock.acquire()
		self._jobs = []
		self.opLock.release()

		# Wait some time to do cleanup
		while len(closingJobs) > 0:
			aux = []
			for i in closingJobs:
				if not i[0].poll():
					i[1] -= 1
					if i[1] > 0:
						aux.append([i[0], i[1]])

			closingJobs = aux
			time.sleep(self.sleepTime)

		self.running = -2

	def loadSettings(self, path):
		self._settings = DCSettings()
		self._settings.load(path)

		if self._settings.ip != None:
			self._localAddress = self._settings.ip
		else:
			self._localAddress = getLocalIP()

		if len(self._settings.share) > 0:
			acc = 0L
			for i in self._settings.share:
				l = DCLocalList(i)
				acc += l.getSize()
				self._localLists.append(l)

			self._settings.user.share = acc
			DCLocalListWriter().write("MyList.DcLst", self._localLists)

		try:
			port = self._settings.port
			if self._settings.active == 0: port = 0

			self._searchWorker = DCSearchWorker("0.0.0.0", port)
			self._xferListener = DCXferListener("0.0.0.0", port)
		except socket.error, e:
			if e[0] == 13:
				print "You don't have permissions to bind a socket to port", str(self._settings.port) + "."
				print "Try running pyDC as root."
			else:
				raise e
			sys.exit(-1)

		self._queue = DCQueue()
		try: self._queue.load()
		except IOError: pass

	def addJob(self, job):
		if isinstance(job, DCHub):
			if job.getAddress() == None:
				return

		self.opLock.acquire()
		self.addedJobs[job] = 1
		self.opLock.release()

		if isinstance(job, DCHub):
			self.lock.acquire()
			for listener in self.listeners:
				listener.onNewHub(job)
			self.lock.release()

	def removeJob(self, job):
		self.opLock.acquire()
		self.removedJobs[job] = 1
		self.opLock.release()

	def refreshLocalList(self):
		# TODO: this is not xfer safe!
		self.opLock.acquire()

		acc = 0L
		for l in self._localLists:
			l.scan()
			acc += l.getSize()

		self._settings.user.share = acc
		DCLocalListWriter().write("MyList.DcLst", self._localLists)

		self.opLock.release()

		for hub in self.getHubs():
			hub.updateInfo()

	def deregisterAllListeners(self):
		self.lock.acquire()
		self._searchWorker.deregisterAllListeners()
		self._xferListener.deregisterAllListeners()
		self._queue.deregisterAllListeners()
		
		for i in self._jobs:
			try: i.deregisterAllListeners()
			except AttributeError: pass
		self.lock.release()

	###################
	# Private members #
	###################

	def acquireSlot(self):
		self.opLock.acquire()
		retval = 0
		if self._usedSlots < self._settings.slots:
			self._usedSlots += 1
			retval = 1
		self.opLock.release()

		return retval

	def releaseSlot(self):
		self.opLock.acquire()
		if self._usedSlots > 0:
			self._usedSlots -= 1
		self.opLock.release()

	settings = property(getSettings, None, None, None)
	user = property(getUser, None, None, None)
	localAddress = property(getLocalAddress, None, None, None)
	searchWorker = property(getSearchWorker, None, None, None)
	xferListener = property(getXferListener, None, None, None)
	queue = property(getQueue, None, None, None)
	hubs = property(getHubs, None, None, None)
	jobs = property(getJobs, None, None, None)
	xfers = property(getXfers, None, None, None)
	usedSlots = property(getUsedSlots, None, None, None)

class SettingsException(Exception): pass

#Global object
sys.modules['__main__'].dcWorker = DCWorker()

def getWorker():
	return sys.modules['__main__'].dcWorker
