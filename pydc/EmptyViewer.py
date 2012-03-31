# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
from JobViewerInfo import *
from Util import *

class EmptyViewer(wxPanel):
	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)
		wnd = getMainWnd()

	def getTitle(self):
		return ''

	def getInfo(self):
		return EmptyViewerInfo()

class EmptyViewerInfo(JobViewerInfo):
	def __init__(self):
		JobViewerInfo.__init__(self, None)
