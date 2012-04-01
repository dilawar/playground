# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class ViewerListener:
	def onViewerTitle(self, viewer, title):
		pass

	def onViewerClosed(self, viewer, jobStopped):
		pass
