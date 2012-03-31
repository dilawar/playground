# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
from Util import *
from ViewerListener import *

from DCSearch import *
from DCSearchWorkerEventListener import *
from DCSearchEventListener import *
import DCWorker

class SearchesPanel(wxPanel, ViewerListener, DCSearchWorkerEventListener, DCSearchEventListener):
	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)
		
		self.searches = []
		self.sortAlgos = [ None,
		                   (self.getSearchPattern, cmp),
		                   (DCSearch.getResultNum, icmp),

		                   (DCSearch.getResultNum, cmp),
		                   (self.getSearchPattern, icmp) ]
		self.sortAlgo = 1

		self.list = wxListCtrl(self, 1, style = wxLC_REPORT | wxLC_VRULES)
		self.new = wxButton(self, 2, 'New')

		self.list.InsertColumn(0, 'Pattern')
		self.list.InsertColumn(1, 'Hits')
		self.list.Show(1)

		vLayout = wxBoxSizer(wxVERTICAL)

		vLayout.Add(self.list, 1, wxEXPAND)
		vLayout.Add(self.new, 0, wxEXPAND | wxTOP, 5)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_LIST_COL_CLICK(self, 1, self.setSortAlgo)
		EVT_LIST_ITEM_SELECTED(self, 1, self.onSearchActivation)
		EVT_BUTTON(self, 2, self.onSearch)
		self.Connect(1, 1, wxEVT_NULL, self.insertSearch)
		self.Connect(2, 2, wxEVT_NULL, self.updateSearch)
		self.Connect(3, 3, wxEVT_NULL, self.removeSearch)

	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		access, comp = self.sortAlgos[self.sortAlgo]
		self.searches = fullSort(self.searches, access, comp)

		self.list.Freeze()
		pos = 0
		for search in self.searches:
			pattern = search.getPattern()
			if pattern == None: pattern = '[New search]'
			self.list.SetStringItem(pos, 0, pattern)
			self.list.SetStringItem(pos, 1, str(search.getResultNum()))
			pos += 1
		self.list.Thaw()

	def onSearch(self, event):
		search = getMainWnd().newSearch()

	def onNewSearch(self, search):
		if search.isPrivate(): return
		wxPostEvent(self, guiEvent(1, search))

	def onSearchActivation(self, event):
		getMainWnd().setActiveJob(self.searches[event.GetIndex()])

	def onSearchStart(self, search):
		wxPostEvent(self, guiEvent(2, search))

	def onNewResult(self, search, result):
		wxPostEvent(self, guiEvent(2, search))

	def onSearchStop(self, search):
		wxPostEvent(self, guiEvent(3, search))

	def onViewerClosed(self, viewer, stoppedJob):
		event = guiEvent(3, viewer.getInfo().getJob())
		self.removeSearch(event)

	#=================#
	# Private section #
	#=================#

	def getSearchPattern(self, search):
		return search.getPattern().lower()

	def insertSearch(self, event):
		search = event.data
		search.registerListener(self)

		try:
			self.searches.index(search)
 			return
		except ValueError:
			self.searches.append(search)

		self.sortList()
		pos = self.searches.index(search)

		pattern = search.getPattern()
		if pattern == None: pattern = '[New search]'
		self.list.InsertStringItem(pos, pattern)
		self.list.SetStringItem(pos, 1, str(search.getResultNum()))

	def updateSearch(self, event):
		search = event.data

		oldPos = self.searches.index(search)
		self.sortList()
		pos = self.searches.index(search)

		if oldPos == pos:
			self.list.SetStringItem(pos, 0, search.getPattern())
			self.list.SetStringItem(pos, 1, str(search.getResultNum()))
		else:
			self.list.DeleteItem(oldPos)
			self.list.InsertStringItem(pos, search.getPattern())
			self.list.SetStringItem(pos, 1, str(search.getResultNum()))

	def removeSearch(self, event):
		try:
			pos = self.searches.index(event.data)
			del self.searches[pos]
			self.list.DeleteItem(pos)
		except ValueError:
			return

	def sortList(self):
		if len(self.searches) < 2: return

		if self.sortAlgo == 0:
			return
		elif self.sortAlgo == 1:
			self.searches.sort(lambda x, y: cmp(x.getPattern(), y.getPattern()))
		elif self.sortAlgo == -1:
			self.searches.sort(lambda x, y: cmp(y.getPattern(), x.getPattern()))
		elif self.sortAlgo == 2:
			self.searches.sort(lambda x, y: x.getResultNum() - y.getResultNum())
		elif self.sortAlgo == -2:
			self.searches.sort(lambda x, y: y.getResultNum() - x.getResultNum())
