# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from threading import Lock

class EventGenerator:
	def __init__(self):
		self.lock = Lock()
		self.listeners = []

	def registerListener(self, listener):
		self.lock.acquire()
		if not listener in self.listeners:
			self.listeners.append(listener)
		self.lock.release()

	def deregisterListener(self, listener):
		self.lock.acquire()
		try: self.listeners.remove(listener)
		except ValueError: pass
		self.lock.release()

	def deregisterAllListeners(self):
		self.lock.acquire()
		self.listeners = []
		self.lock.release()
