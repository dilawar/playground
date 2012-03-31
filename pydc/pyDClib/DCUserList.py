# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from EventGenerator import *
from Job import *
from he3 import *
from DCQueueItem import *
from DCQueueEventListener import DCQueueEventListener
from DCItem import *
from DCFileList import *
import DCWorker
import os
import thread

class DCUserList(Job, EventGenerator, DCFileList, DCQueueItem, DCQueueEventListener):
	STATUS_INIT = DCQueueItem.STATUS_WAITING-1
	STATUS_WAITING = DCQueueItem.STATUS_WAITING
	STATUS_DOWNLOADING = DCQueueItem.STATUS_RUNNING
	STATUS_DECODING = DCQueueItem.STATUS_COMPLETED
	STATUS_ERROR = DCQueueItem.STATUS_ERROR
	STATUS_COMPLETED = DCQueueItem.STATUS_COMPLETED+100
	STATUS_STOPPED = DCQueueItem.STATUS_COMPLETED+101

	FILENAME_TEMPLATE = "tmp%d.DcLst"
	tmpnum = 0

	def __init__(self, user):
		if not user.hub: raise UserZombieError

		EventGenerator.__init__(self)
		DCFileList.__init__(self)
		self._user = user

		item = DCItem()
		item.userNick = user.nick
		item.path = "MyList.DcLst"

		self.lock.acquire()
		self.num = DCUserList.tmpnum
		DCUserList.tmpnum += 1
		self.lock.release()

		filename = DCWorker.getWorker().getSettings().download + os.sep + self.FILENAME_TEMPLATE % self.num
		try: os.unlink(filename)
		except OSError: pass

		DCQueueItem.__init__(self, item, self.FILENAME_TEMPLATE % self.num)
		self.completed = 0
		self._status = self.STATUS_INIT
		
		DCWorker.getWorker().getQueue().registerListener(self)

	def getUser(self):
		return self._user

	def getPattern(self):
		return None

	def addSource(self, item):
		pass

	def removeSource(self, nick):
		DCWorker.getWorker().xferListener.stopXfer(self, self._sources[0])
		DCWorker.getWorker().getQueue().onItemStatus(self)

	def serialize(self):
		return None

	def onItemRemoved(self, queue, item):
        	if item == self: self.stop()

	###################
	# Private methods #
	###################

	def poll(self):
		if self._status == self.STATUS_INIT:
			self._status = self.STATUS_WAITING
			DCWorker.getWorker().getQueue().addQueueItem(self)

		elif self._status >= self.STATUS_ERROR:
			if self.num < 0: return 1

			if self._status == self.STATUS_ERROR or self._status == self.STATUS_STOPPED:
				DCWorker.getWorker().getQueue().removeItem(self)
				
			filename = DCWorker.getWorker().getSettings().download + os.sep + self.FILENAME_TEMPLATE % self.num
			try: os.unlink(filename)
			except OSError: pass
			self.num = -1

			return 1

		return 0

	def stop(self):
		self.setStatus(self.STATUS_STOPPED)

	def isAlive(self):
		if self._status >= self.STATUS_ERROR:
			return 0
		else:
			return 1

	def sendRequest(self):
		if not self._user.hub:
			self.setStatus(self.STATUS_ERROR)
			DCWorker.getWorker().getQueue().removeItem(self)
			return

		self._user.hub.requireConnection(self._user.nick)

	def setStatusCompleted(self, source):
		retval = DCQueueItem.setStatusCompleted(self, source)
		DCWorker.getWorker().getQueue().removeItem(self)
		thread.start_new_thread(self.parseList, ())

	def setStatus(self, status):
		self.lock.acquire()
		self._status = status
		self.lock.release()

	def parseList(self):
		try:
			filename = DCWorker.getWorker().getSettings().download + os.sep + self.FILENAME_TEMPLATE % self.num
			r = LineReader(He3Decoder().decode(filename))
			self._list = self.populate(r, 0, self)

			self.setStatus(self.STATUS_COMPLETED)
		except IOError:
			self.setStatus(self.STATUS_ERROR)
		except ValueError:
			self.setStatus(self.STATUS_ERROR)
		except He3FormatError:
			self.setStatus(self.STATUS_ERROR)

	def populate(self, r, level, parent):
		l = []

		while 1:
			line = r.get()
			if line == None:
				return l

			lineLevel = 0
			while line[lineLevel] == '\t':
				lineLevel += 1

			if lineLevel < level:
				r.unget()
				return l
			else:
				pos = line.rfind('|')
				if pos == -1:
					d = UserDir(line[lineLevel:], parent, None)
					d.children = self.populate(r, level+1, d)
					l.append(d)
				else:
					l.append(UserFile(line[lineLevel:pos], parent, long(line[pos+1:])))

	user = property(getUser, None, None, None)

class LineReader:
	def __init__(self, data):
		self.lines = data.split('\r\n')
		if len(self.lines[-1]) == 0:
			self.lines = self.lines[:-1]
		self.pos = 0

	def get(self):
		if self.pos >= len(self.lines):
			return None

		line = self.lines[self.pos]
		self.pos += 1
		return line

	def unget(self):
		self.pos -= 1

class UserZombieError(Exception): pass
