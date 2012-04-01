# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from DCItem import *

class DCSearchResult(DCItem):
	def __init__(self):
		DCItem.__init__(self)

		self.type = None
		self.freeSlots = -1
		self.slots = -1
		self.hubName = None

