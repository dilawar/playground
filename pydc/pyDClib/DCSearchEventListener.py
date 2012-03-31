# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCSearchEventListener:
	def onSearchStart(self, search):
		pass
		
	def onSearchStop(self, search):
		pass

	def onNewResult(self, search, result):
		pass
