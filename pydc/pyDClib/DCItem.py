# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCItem:
	def __init__(self):
		self.userNick = None
		self.path = None
		self.size = -1L

	def copy(self, item):
		self.userNick = item.userNick
		self.path = item.path
		self.size = item.size

	def getPath(self):
		return self.path
		
	def getSize(self):
		return self.size
