# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
from wx.py import shell
from ViewerListener import *
from HublistPanel import *
from ViewsPanel import *
from HubsPanel import *
from QueuePanel import *
from XfersPanel import *
from SearchesPanel import *
from EmptyViewer import *
from HubViewer import *
from ChatViewer import *
from SearchViewer import *

from DCHublistRetriever import *
from DCHub import *
from DCSearch import *
import DCWorker

class MainWnd(wxFrame, ViewerListener):
	def __init__(self, parent, id, title):
		wxFrame.__init__(self, parent, -1, title, size = (640, 480), style = wxDEFAULT_FRAME_STYLE)

		self.infos = JobInfos()
		self.chatEnabled = 1
		self.timer = wxTimer(self)

		self.hSplit = wxSplitterWindow(self, -1, style = wxNO_3D | wxSP_NOBORDER)

		self.vSplit = wxSplitterWindow(self.hSplit, -1, style = wxNO_3D | wxSP_3D)
		self.vSplit.SetMinimumPaneSize(5)

		self.notebook = wxNotebook(self.vSplit, 1)

		self.hublist = HublistPanel(self.notebook, -1)
		self.notebook.AddPage(self.hublist, 'Hublist')
		
		self.views = ViewsPanel(self.notebook, -1)
		self.notebook.AddPage(self.views, 'Views')

		self.hubs = HubsPanel(self.notebook, -1)
		self.notebook.AddPage(self.hubs, 'Hubs')

		self.queue = QueuePanel(self.notebook, -1)
		self.notebook.AddPage(self.queue, 'Queue')

		self.xfers = XfersPanel(self.notebook, -1)
		self.notebook.AddPage(self.xfers, 'Xfers')
		
		self.searches = SearchesPanel(self.notebook, -1)
		self.notebook.AddPage(self.searches, 'Searches')

		self.viewer = EmptyViewer(self.vSplit, -1)
		
		self.shell = shell.Shell(self.hSplit, -1)
		self.shell.autoComplete = 0
		self.shell.interp.runsource('from InterUtils import *')

		self.vSplit.SplitVertically(self.notebook, self.viewer)
		self.hSplit.SplitHorizontally(self.vSplit, self.shell)

		self.Show(1)
		self.hSplit.SetSashPosition(380, 1)
		self.vSplit.SetSashPosition(350, 1)
		self.oldHeight = self.hSplit.GetSize().GetHeight()

		self.hublist.text.SetFocus()
		
		# Event handlers
                EVT_SIZE(self.hSplit, self.onSplitSize)
		EVT_CLOSE(self, self.onClose)
		EVT_TIMER(self, -1, self.onTimer)

		# Accelerators
		self.SetAcceleratorTable(wxAcceleratorTable([(wxACCEL_CTRL, ord('S'), 1000),
		                                             (wxACCEL_CTRL, ord('Q'), 1001)]))
		EVT_MENU(self, 1000, self.newSearch)
		EVT_MENU(self, 1001, self.onClose)
		
		# Final setup
		worker = DCWorker.getWorker()
		#retriever = DCHublistRetriever()
		#retriever.registerListener(self.hublist)
		#worker.addJob(retriever)
		worker.registerListener(self.hubs)
		worker.getSearchWorker().registerListener(self.searches)
		self.timer.Start(3000)

	def onSplitSize(self, sizeEvent):
		newHeight = sizeEvent.GetSize().GetHeight()
		pos = self.hSplit.GetSashPosition() + newHeight - self.oldHeight
		self.hSplit.SetSashPosition(pos)
		self.oldHeight = newHeight

		sizeEvent.Skip()

	def onClose(self, closeEvent):
		DCWorker.getWorker().deregisterAllListeners()
		self.Destroy()

	def onTimer(self, event):
		self.hubs.update()
		self.xfers.update()

	def setActiveJob(self, job):
		oldViewer = self.viewer
		if job == oldViewer.getInfo().getJob():
			return

		info = self.infos.peek(job)
		if info == None:
			if isinstance(job, DCHub):
				info = HubViewerInfo(job)
			elif isinstance(job, ChatJob):
				info = ChatViewerInfo(job)
			elif isinstance(job, DCSearch):
				info = SearchViewerInfo(job)

		self.setupViewer(info)
		self.infos.add(job, self.viewer.getInfo())
		self.activateViewer()

		oldViewer.Destroy()

	def getActiveJob(self):
		return self.viewer.getInfo().getJob()

	def connectToHub(self, addr, show = 1):
		hub = DCHub(addr)
		if show: self.setActiveJob(hub)
		DCWorker.getWorker().addJob(hub)
		return hub

	def getChat(self, nick, hub):
		if not self.chatEnabled: return None

		chat = self.infos.searchChat(nick, hub.getAddress())
		if chat:
			return chat
		else:
			chat = ChatJob(nick, hub)
			self.setActiveJob(chat)
			return chat

	def newSearch(self, dummy=None):
		search = DCSearch()
		self.setActiveJob(search)
		self.searches.onNewSearch(search)
		return search

	def onViewerTitle(self, viewer, title):
		if isinstance(viewer, HubViewer):
			title = '- Hub: ' + title
		elif isinstance(viewer, ChatViewer):
			title = '- Chat: ' + title
		elif isinstance(viewer, SearchViewer):
			title = '- Search: ' + title

		self.SetTitle('pyDC %s' % title)

	def onViewerClosed(self, viewer, jobStopped):
		job = self.viewer.getInfo().getJob()
		info = self.infos.remove(job)

		if info:
			self.setupViewer(info)
		else:
			self.viewer = EmptyViewer(self.vSplit, -1)
			self.viewer.SetFocus()   #needed to make accelerators work

		self.activateViewer()

	#===================#
	#  Private members  #
	#===================#

	def setupViewer(self, info):
		if isinstance(info, HubViewerInfo):
			self.viewer = HubViewer(self.vSplit, -1, info)

		elif isinstance(info, ChatViewerInfo):
			self.viewer = ChatViewer(self.vSplit, -1, info)

		elif isinstance(info, SearchViewerInfo):
			self.viewer = SearchViewer(self.vSplit, -1, info)
			self.viewer.registerListener(self.searches)

		self.viewer.registerListener(self)

		self.views.onNewViewer(self.viewer)
		self.viewer.registerListener(self.views)

	def activateViewer(self):
		sashPos = self.vSplit.GetSashPosition()
		self.vSplit.Unsplit()
		self.vSplit.SplitVertically(self.notebook, self.viewer, sashPos)

		self.onViewerTitle(self.viewer, self.viewer.getTitle())

class JobInfos:
	def __init__(self):
		self.l = []

	def add(self, job, info):
		self.l.append((job, info))

	def remove(self, job):
		try:
			if self.l[-1] == job:
				del self.l[-1]
			else:
				self.peek(job)

			return self.l[-1][1]
		except IndexError:
			return None

	def peek(self, job):
		num = 0
		for pair in self.l:
			if pair[0] == job:
				del self.l[num]
				return pair[1]
			num += 1

		return None

	def searchChat(self, nick, address):
		num = 0
		for pair in self.l:
			if isinstance(pair[0], ChatJob):
				if pair[0].getNick() == nick and pair[0].getAddress() == address:
					del self.l[num]
					self.l.append(pair)
					return pair[0]
			num += 1

		return None

