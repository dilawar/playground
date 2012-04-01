# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from copy import copy
from threading import Lock
import pickle
import time

from DCQueueItem import *
from DCSourceSearch import *
from EventGenerator import *
from Job import *
import DCWorker

class DCQueue(object, Job, EventGenerator):
	EVENT_NEW = 0
	EVENT_REMOVED = 1
	EVENT_STATUS = 2

	RETRY_TIME = 30

	SAVE_DELAY = 15
	QUEUE_FILE = 'queue.pk'

	SEARCH_TRIGGER = 10
	SEARCH_INTERVAL = 30

	def __init__(self):
		EventGenerator.__init__(self)
		
		self.opLock = Lock()
		self._items = []
		self.status = 0
		self.saveTime = 0
		self.searchTime = 0
		self.searchCursor = -1

	def addItem(self, item, path = None):
		queueItem = DCQueueItem(item, path)
		self.addQueueItem(queueItem)
		return queueItem

	def addQueueItem(self, item):
		self.opLock.acquire()
		for i in self._items:
			if i.path == item.getPath():
				self.opLock.release()
				raise ItemAlreadyAddedError

		self._items.append(item)
		self.saveTime = time.time() + self.SAVE_DELAY
		self.opLock.release()

		self.fireEvent(self.EVENT_NEW, item)

	def getItems(self):
		self.opLock.acquire()
		items = copy(self._items)
		self.opLock.release()

		return items

	def removeItem(self, item):
		try:
			self.opLock.acquire()
			self._items.remove(item)
			DCWorker.getWorker().xferListener.stopXfer(item)
			self.saveTime = time.time() + self.SAVE_DELAY
			self.opLock.release()
		except ValueError:
			self.opLock.release()
			return
		
		self.fireEvent(self.EVENT_REMOVED, item)

	def getItemByNick(self, nick):
		item = None
		source = None

		self.opLock.acquire()
		for i in self._items:
			if i.status == DCQueueItem.STATUS_WAITING:
				for s in i.sources:
					if s.nick == nick:
						item = i
						source = s
						break
		self.opLock.release()

		return item, source

	def load(self):
		self.opLock.acquire()
		try: aux = pickle.load(open(self.QUEUE_FILE, 'rb'))
		except IOError, e:
			self.opLock.release()
			raise e

		for item in aux:
			self._items.append(DCQueueItem(item))
		self.opLock.release()

	def save(self):
		self.opLock.acquire()
		aux = []
		for item in self._items:
			serialized = item.serialize()
			if serialized: aux.append(item.serialize())

		try: pickle.dump(aux, open(self.QUEUE_FILE, 'wb'))
		except IOError, e:
			self.opLock.release()
			raise e

		self.saveTime = 0
		self.opLock.release()

	def poll(self):
		if self.status == 0:
			curTime = time.time()
			canSearch = curTime - self.searchTime > self.SEARCH_INTERVAL

			self.opLock.acquire()

			pos = 0
			for item in self._items:
				if curTime - item._timestamp > DCQueue.RETRY_TIME:
					if item.status == DCQueueItem.STATUS_WAITING:
						item.sendRequest()

						if self.SEARCH_TRIGGER > 0 and pos > self.searchCursor and isinstance(item, DCQueueItem):
							if item._retries > self.SEARCH_TRIGGER and canSearch:
								DCSourceSearch(item).start()
								self.searchTime, self.searchCursor, canSearch,  = curTime, pos, 0
								item._retries = 0
							else:
								item._retries += 1

					item._timestamp = curTime

				pos += 1

			if self.searchCursor == pos-1:
				self.searchCursor = -1

			self.opLock.release()

			if self.saveTime != 0 and self.saveTime < curTime:
				self.save()

		elif self.status == 1:
			return 1

		return 0

	def stop(self):
		self.status = 1

	def isAlive(self):
		return self.status == 0
		
	def onItemStatus(self, item):
		try:
			self.opLock.acquire()
			self._items.index(item)
			self.opLock.release()

			self.fireEvent(self.EVENT_STATUS, item)
		except ValueError:
			self.opLock.release()
			
	def onItemSourceChange(self, item):
		self.opLock.acquire()
		self.saveTime = time.time() + self.SAVE_DELAY
		self.opLock.release()

	###################
	# Private members #
	###################

	def fireEvent(self, event, item):
		self.lock.acquire()
		for listener in self.listeners:
			if event == DCQueue.EVENT_NEW:
				listener.onNewItem(self, item)
			elif event == DCQueue.EVENT_REMOVED:
				listener.onItemRemoved(self, item)
			elif event == DCQueue.EVENT_STATUS:
				listener.onItemStatus(self, item)
		self.lock.release()

	items = property(getItems, None, None, None)

class ItemAlreadyAddedError(Exception): pass
