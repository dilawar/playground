# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from threading import Lock
import os
import os.path
import random

from DCItem import DCItem
import DCWorker

class DCQueueItem(object):
	STATUS_WAITING = 0
	STATUS_RUNNING = 1
	STATUS_COMPLETED = 2
	STATUS_ERROR = 3

	def __init__(self, item, path = None):
		if isinstance(item, DCItem):
			self._sources = [DCQueueItemSource(item.userNick, item.path)]

			base = DCWorker.getWorker().getSettings().download
			if path:
				self._path = os.path.abspath(base + os.sep + path)

				if len(self._path) < len(base):
					raise IllegalLocalPathError

				if self._path[:len(base)] != base:
					raise IllegalLocalPathError
			else:
				self._path = base + os.sep + item.path[item.path.rindex('\\')+1:]

			self._status = self.STATUS_WAITING
			self._progress = 0
		elif isinstance(item, DCSerializedQueueItem):
			self._path = item.path
			self._status = item.status
			self._progress = item.progress
			self._sources = item.sources
		else:
			raise IllegalItem

		self._size = item.size
		self._xfer = None
		self._timestamp = 0
		self._retries = 0
		self.lock = Lock()

	def addSource(self, item):
		if self._size != item.size:
			raise ItemNotMatching

		self.lock.acquire()
		for source in self._sources:
			if source.nick == item.userNick and source.path == item.path:
				self.lock.release()
				raise ExistingSourceError

		self._sources.append(DCQueueItemSource(item.userNick, item.path))
		self._timestamp = 0

		statusUpd = 0
		if self._status == DCQueueItem.STATUS_ERROR:
			self._status = DCQueueItem.STATUS_WAITING
			statusUpd = 1

		self.lock.release()

		DCWorker.getWorker().getQueue().onItemSourceChange(self)
		if statusUpd: DCWorker.getWorker().getQueue().onItemStatus(self)

	def removeSource(self, nick):
		self.lock.acquire()
		aux = None
		for i in range(0, len(self._sources)):
			if self._sources[i].nick == nick:
				aux = self._sources[i]
				del self._sources[i]
				break
		self.lock.release()

		worker = DCWorker.getWorker()
		if aux:
			worker.xferListener.stopXfer(self, aux)

			if len(self._sources) == 0:
				self._status = self.STATUS_ERROR
				worker.getQueue().onItemStatus(self)

			worker.getQueue().onItemSourceChange(self)

	def serialize(self):
		self.lock.acquire()
		data = DCSerializedQueueItem(self._path, self._size, self._status, self._progress, self._sources)
		self.lock.release()
		return data

	def getOnlineSources(self):
		self.lock.acquire()
		nicks = []
		for source in self._sources:
			nicks.append(source._nick)
		self.lock.release()

		aux = []
		for nick in nicks:
			for user in DCWorker.getWorker().getUsersByNick(nick):
				aux.append(user)

		return aux

	def getSources(self):
		self.lock.acquire()
		sources = []
		for source in self._sources:
			sources.append(source)
		self.lock.release()

		return sources

	def getPath(self):
		return self._path

	def getSize(self):
		return self._size

	def getStatus(self):
		return self._status

	def getProgress(self):
		return self._progress
		
	def getXfer(self):
		return self._xfer

	def getPattern(self):
		self.lock.acquire()
		source = self._sources[random.randint(0, len(self._sources)-1)]
		self.lock.release()

		pattern, path = '', source.getPath()
		path = path[path.rindex('\\')+1:]
		for c in path:
			if c.isalnum():
				pattern += c
			else:
				pattern += ' '

		return pattern.strip()

	def setStatusRunning(self, source):
		self.lock.acquire()
		if self._status != self.STATUS_WAITING:
			retval = 0
		else:
			self._status = self.STATUS_RUNNING
			self._xfer = source
			retval = 1
		self.lock.release()

		if retval: DCWorker.getWorker().getQueue().onItemStatus(self)
		return retval

	def setStatusWaiting(self, source):
		self.lock.acquire()
		if self._xfer != source:
			retval = 0
		else:
			if self._status == self.STATUS_RUNNING:
				self._status = self.STATUS_WAITING
			self._xfer = None
			retval = 1
		self.lock.release()

		if retval: DCWorker.getWorker().getQueue().onItemStatus(self)
		return retval

	def setStatusCompleted(self, source):
		self.lock.acquire()
		if self._xfer != source:
			retval = 0
		else:
			self._status = self.STATUS_COMPLETED
			self._progress = 100
			self._xfer = None
			retval = 1
		self.lock.release()

		if retval: DCWorker.getWorker().getQueue().onItemStatus(self)
		return retval

	###################
	# Private methods #
	###################

	def sendRequest(self):
		for user in self.getOnlineSources():
			user.hub.requireConnection(user.nick)

	def setSize(self, size):
		self._size = size

	def setProgress(self, progress):
		self._progress = progress

	sources = property(getSources, None, None, None)
	onlineSources = property(getOnlineSources, None, None, None)
	path = property(getPath, None, None, None)
	size = property(getSize, None, None, None)
	status = property(getStatus, None, None, None)
	progress = property(getProgress, None, None, None)
	xfer = property(getXfer, None, None, None)

class DCQueueItemSource:
	def __init__(self, nick, path):
		self._nick = nick
		self._path = path

	def getNick(self):
		return self._nick

	def getPath(self):
		return self._path

	nick = property(getNick, None, None, None)
	path = property(getPath, None, None, None)
	
class DCSerializedQueueItem:
	def __init__(self, path, size, status, progress, sources):
		self.path = path
		self.size = size
		self.status = status
		self.progress = progress
		self.sources = sources
		
		if self.status == DCQueueItem.STATUS_RUNNING:
			self.status = DCQueueItem.STATUS_WAITING

class IllegalItem(Exception): pass
class IllegalLocalPathError(Exception): pass
class ItemNotMatching(Exception): pass
class ExistingSourceError(Exception): pass
