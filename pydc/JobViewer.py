# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
import time

class JobViewer:
	def __init__(self, info):
		self.info = info
		self.processEvents = 1

		self.info.getJob().registerListener(self)
		
	def __del__(self):
		self.processEvents = 0
		self.SetEvtHandlerEnabled(0)
		
		try: wxYield()
		except: pass
		self.info.getJob().deregisterListener(self)

	def getTitle(self):
		pass
		
	def getInfo(self):
		return self.info
