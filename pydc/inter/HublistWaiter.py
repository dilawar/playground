# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from DCHublistRetriever import *
from DCHublistRetrieverEventListener import *
import DCWorker

class HublistWaiter(DCHublistRetrieverEventListener):
	SLEEP = 0.5

	def __init__(self):
		self.lock = Lock()
		self.list = []

		retr = DCHublistRetriever()
		retr.registerListener(self)
		self.lock.acquire()
		DCWorker.getWorker().addJob(retr)

	def onHublist(self, list):
		self.list = list
		self.lock.release()

	def wait(self):
		while 1:
			if self.lock.acquire(0): return 1
			time.sleep(self.SLEEP)

