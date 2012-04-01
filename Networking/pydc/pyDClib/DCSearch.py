# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from EventGenerator import *
import DCWorker
from threading import Lock
from copy import copy
import socket
import string
import os
import time

class DCSearch(object, EventGenerator):
	LOG_STATUS = 1
	LOG_CHAT = 2
	LOG_ERROR = 3

	def __init__(self, pattern = None, private = 0):
		EventGenerator.__init__(self)

		self._pattern = pattern
		self._results = []
		self._private = private
		self._status = 0
		self.opLock = Lock()

	def getStatus(self):
		return self._status

	def setPattern(self, pattern):
		if self._status != 0:
			raise SearchInProgressError()
		self._pattern = pattern

	def getPattern(self):
		return self._pattern
		
	def isPrivate(self):
		return self._private

	def getResultNum(self):
		return len(self._results)

	def getResults(self):
		self.opLock.acquire()
		results = copy(self._results)
		self.opLock.release()

		return results

	def start(self, nodelay=0):
		if self._pattern == None:
			raise PatternNotSetError()

		res = DCWorker.getWorker().getSearchWorker().registerSearch(self, nodelay)
		if res:
			self.lock.acquire()
			for listener in self.listeners:
				listener.onSearchStart(self)
			self.lock.release()
			self._status = 1

		return res

	def stop(self):
		if self._status == 1:
			DCWorker.getWorker().getSearchWorker().deregisterSearch(self)
			self._status = 2
			
			self.lock.acquire()
			for listener in self.listeners:
				listener.onSearchStop(self)
			self.lock.release()

	def isAlive(self):
		return self._status == 1

	def onNewResult(self, result):
		resultPath = result.path.lower()
		try:
			for i in self._pattern.lower().split(' '): resultPath.index(i)
		except ValueError:
			return

		self.opLock.acquire()
		self._results.append(result)
		self.opLock.release()
		
		self.lock.acquire()
		for listener in self.listeners:
			listener.onNewResult(self, result)
		self.lock.release()

	#=================#
	# Private section #
	#=================#

	status = property(getStatus, None, None, None)
	pattern = property(getPattern, setPattern, None, None)
	private = property(isPrivate, None, None, None)
	resultNum = property(getResultNum, None, None, None)
	results = property(getResults, None, None, None)

class PatternNotSetError(Exception): pass
class SearchInProgressError(Exception): pass
