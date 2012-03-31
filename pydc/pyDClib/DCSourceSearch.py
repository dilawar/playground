# This file is part of pyDC software
# Copyright 2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from DCQueueItem import ExistingSourceError
import DCWorker

class DCSourceSearch:
	def __init__(self, item):
		self._item = item
		self._pattern = item.getPattern()
		self._size = item.getSize()

	def start(self):
		if self._pattern == None or len(self._pattern) == 0: return

		DCWorker.getWorker().getSearchWorker().registerSearch(self, 1)

	def stop(self):
		DCWorker.getWorker().getSearchWorker().deregisterSearch(self)

	def onNewResult(self, result):
		resultPath = result.path.lower()
		try:
			for i in self._pattern.lower().split(' '): resultPath.index(i)
		except ValueError:
			return

		if result.getSize() != self._size:
			return

		try: self._item.addSource(result)
		except ExistingSourceError: return

		print "Added new source to:", self._item.getPath()

	def getPattern(self):
		return self._pattern

	def isPrivate(self):
		return 1

