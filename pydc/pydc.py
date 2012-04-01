# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
from socket import error
import sys

sys.path.append("./pyDClib/")

from MainWnd import *
from DCSettings import *
from DCHublistRetriever import *
from DCQueueItem import IllegalItem
import DCWorker

wnd = None

welcome = '''
+------------------------------------------------------------------+
| iitbDC                                                           |
| Direct Connect client written in Python.                         |
|                                                                  |
| Originally pyDC by Anakim Border <aborder@users.sourceforge.net> |
| Maintained by Dilawar Singh <dilawar@ee.iitb.ac.in>              |
| Version 0.62                                                     |
+------------------------------------------------------------------+
'''
print welcome

class App(wxApp):
	def OnInit(self):
		global wnd

		worker = DCWorker.getWorker()
		try: worker.loadSettings("settings.xml")
		except ParseError, e:
			print e
			return 0
		except IllegalItem:
			print 'The file \'queue.pk\' is corrupted. Please remove it and restart pyDC.'
			return 0
		except error:
			print 'Address already in use. Maybe there\'s another pyDC instance already running.\nIf not, please wait a minute and retry.'
			return 0

		sys.modules['__main__'].hublist = []

		#wnd = MainWnd(None, -1, "pyDC")
		#self.SetTopWindow(wnd)

		#Start the show...
    #worker.start()

		return 1

if __name__ == "__main__":
	app = App(0)
	app.MainLoop()
