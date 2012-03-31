# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from ChatViewer import ChatJob
from Util import *
from ViewerListener import *
from wxPython.wx import *

from DCHub import DCHub
from DCSearch import DCSearch

class ViewsPanel(wxPanel, ViewerListener):
	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)

		self.jobs = []

		self.list = wxListCtrl(self, 1, style = wxLC_REPORT | wxLC_SINGLE_SEL | wxLC_VRULES)

		self.list.InsertColumn(0, "Type")
		self.list.InsertColumn(1, "Name")

		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.list, 1, wxEXPAND | wxTOP, 5)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_LIST_ITEM_SELECTED(self.list, 1, self.onViewerActivation)
		self.Connect(1, 1, wxEVT_NULL, self.insertViewer)
		self.Connect(2, 2, wxEVT_NULL, self.setTitle)
		self.Connect(3, 3, wxEVT_NULL, self.removeViewer)

	def onNewViewer(self, viewer):
		wxPostEvent(self, guiEvent(1, self.snap(viewer)))

	def onViewerTitle(self, viewer, title):
		wxPostEvent(self, guiEvent(2, (viewer.getInfo().getJob(), title)))

	def onViewerActivation(self, event):
		getMainWnd().setActiveJob(self.jobs[event.GetIndex()])

	def onViewerClosed(self, viewer, jobStopped):
		wxPostEvent(self, guiEvent(3, viewer.getInfo().getJob()))

	#=================#
	# Private section #
	#=================#

	def snap(self, viewer):
		job = viewer.getInfo().getJob()

		if isinstance(job, DCHub):
			t = 'Hub'
		elif isinstance(job, ChatJob):
			t = 'Chat'
		elif isinstance(job, DCSearch):
			t = 'Search'

		title = viewer.getTitle()

		return (job, t, title)

	def insertViewer(self, event):
		job = event.data[0]

		try:
			self.jobs.index(job)
			return
		except ValueError:
			self.jobs.append(job)

		self.sortList()
		pos = self.jobs.index(job)

		self.list.InsertStringItem(pos, event.data[1])
		self.list.SetStringItem(pos, 1, event.data[2])

	def setTitle(self, event):
		job = event.data[0]
		title = event.data[1]
		self.list.SetStringItem(self.jobs.index(job), 1, title)

	def removeViewer(self, event):
		pos = self.jobs.index(event.data)
		del self.jobs[pos]
		self.list.DeleteItem(pos)

	def getJobCode(self, job):
		if isinstance(job, ChatJob):
			return 2
		elif isinstance(job, DCHub):
			return 1
		elif isinstance(job, DCSearch):
			return 0

	def compareJobs(self, x, y):
		return self.getJobCode(y) - self.getJobCode(x)

	def sortList(self):
		if len(self.jobs) < 2: return
		self.jobs.sort(self.compareJobs)
