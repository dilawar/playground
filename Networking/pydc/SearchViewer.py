# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os.path
from threading import Lock
from wxPython.wx import *
from EventGenerator import *
from JobViewer import *
from JobViewerInfo import *
from Util import *

from DCSearch import *
from DCSearchEventListener import *
from DCQueue import ItemAlreadyAddedError
from DCQueueItem import *
import DCWorker

class SearchViewer(wxPanel, EventGenerator, DCSearchEventListener, JobViewer):
	def __init__(self, parent, id, info):
		wxPanel.__init__(self, parent, id)
		EventGenerator.__init__(self)
		JobViewer.__init__(self, info)

		self.results = self.info.getJob().getResults()
		self.menuId = -1

		patternLabel = wxStaticText(self, -1, "Pattern:")
		self.patternText = wxTextCtrl(self, 1, style = wxTE_PROCESS_ENTER)
		self.start = wxButton(self, 2, 'Start')
		self.list = wxListCtrl(self, 3, style = wxLC_REPORT | wxLC_VRULES | wxLC_SINGLE_SEL)
		close = wxButton(self, 4, 'Close')

		self.list.InsertColumn(0, "User")
		self.list.InsertColumn(1, "File")
		self.list.InsertColumn(2, "Type")
		self.list.InsertColumn(3, "Size", wxLIST_FORMAT_RIGHT)
		self.list.InsertColumn(4, "Slots")
		self.list.InsertColumn(5, "Connection")
		self.list.InsertColumn(6, "Hub")
		
		hLayout = wxBoxSizer(wxHORIZONTAL)
		hLayout.Add(patternLabel, 0)
		hLayout.Add(self.patternText, 1, wxEXPAND | wxLEFT, 5)

		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(hLayout, 0, wxEXPAND | wxLEFT | wxTOP | wxRIGHT, 5)
		vLayout.Add(self.start, 0, wxALIGN_CENTER | wxTOP, 2)
		vLayout.Add(self.list, 1, wxEXPAND | wxLEFT | wxTOP | wxRIGHT, 5)
		vLayout.Add(close, 0, wxALIGN_CENTER | wxBOTTOM | wxTOP, 5)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_BUTTON(self, 2, self.onStart)
		EVT_BUTTON(self, 4, self.onClose)
		EVT_LIST_COL_CLICK(self, 3, self.setSortAlgo)
		EVT_LIST_ITEM_RIGHT_CLICK(self, 3, self.onResultOptions)
		EVT_LIST_ITEM_ACTIVATED(self, 3, self.onResultSelected)
		EVT_MENU_RANGE(self.list, 0, 10001, self.onPopupSelection)
		self.Connect(1, 1, wxEVT_NULL, self.refreshList)
		self.Connect(2, 2, wxEVT_NULL, self.addResult)

		if self.info.pattern != None:
			self.patternText.SetValue(self.info.pattern)
			
		if self.info.getJob().isAlive():
			self.patternText.Enable(0)
			self.start.Enable(0)

			self.refreshList()
		else:
			self.patternText.SetInsertionPoint(self.info.insertionPoint)
			self.patternText.SetFocus()
			EVT_TEXT_ENTER(self, 1, self.onStart)
			
	def Destroy(self):
		self.info.pattern = self.patternText.GetValue()
		self.info.insertionPoint = self.patternText.GetInsertionPoint()
	
		JobViewer.__del__(self)
		return wxPanel.Destroy(self)
		
	def getTitle(self):
		if self.info.pattern != None:
			return self.info.pattern
		else:
			return '[New search]'

	def onStart(self, event):
		self.info.pattern = self.patternText.GetValue()
		if len(self.info.pattern) == 0:
			dialog = wxMessageDialog(self, 'No pattern present.', 'Search error', wxOK | wxICON_ERROR)
			dialog.ShowModal()
			return
		
		self.patternText.Enable(0)
		self.start.Enable(0)

		job = self.info.getJob()
		job.setPattern(self.info.pattern)
		job.start()
		
		self.lock.acquire()
		for listener in self.listeners:
			listener.onViewerTitle(self, self.info.pattern)
		self.lock.release()

	def onClose(self, event):
		self.lock.acquire()
		self.info.getJob().stop()
		for listener in self.listeners:
			listener.onViewerClosed(self, 1)
		self.lock.release()
		
		self.Destroy()

	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.info.sortAlgo == col:
			self.info.sortAlgo = -col
		else:
			self.info.sortAlgo = col

		wxPostEvent(self, wxPyEvent(1))

	def onResultSelected(self, event):
		try:
			DCWorker.getWorker().getQueue().addItem(self.results[event.GetIndex()])
		except ItemAlreadyAddedError:
			dialog = wxMessageDialog(self, "Item already queued.", "Error", wxICON_ERROR)
			dialog.ShowModal()

	def onResultOptions(self, event):
		pnt = event.GetPoint()
		result = self.results[event.GetIndex()]
		self.list.SetItemState(event.GetIndex(), wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

		menu = wxMenu()
		menu.Append(10000, 'Queue')
		menu.Append(10001, 'Path')
		
		alt, items, pos = wxMenu(), [], 0
		for item in DCWorker.getWorker().getQueue().getItems():
			if item.getStatus() != DCQueueItem.STATUS_COMPLETED and result.size == item.getSize():
				alt.Append(pos, os.path.basename(item.getPath()))
				items.append(item)
				pos += 1
		if pos > 0: menu.AppendMenu(1, 'Source for', alt)

		self.list.PopupMenu(menu, pnt)

		if self.menuId == -1: return
		elif self.menuId == 10000:
			try: DCWorker.getWorker().getQueue().addItem(result)
			except ItemAlreadyAddedError:
				dialog = wxMessageDialog(self, "Item already queued.", "Error", wxICON_ERROR)
				dialog.ShowModal()
		elif self.menuId == 10001:
			wxMessageBox(result.path);
		else:
			try: items[self.menuId].addSource(result)
			except ExistingSourceError: pass
			except ItemNotMatching:
				dialog = wxMessageDialog(self, "Source is not matching.", "Error", wxICON_ERROR)
				dialog.ShowModal()
		self.menuId = -1

	def onPopupSelection(self, event):
		self.menuId = event.GetId()

	def onNewResult(self, search, result):
		wxPostEvent(self, guiEvent(2, result))

	#=================#
	# Private section #
	#=================#

	def refreshList(self, event=None):
		if len(self.results) == 0: return
		self.sortList()

		self.list.DeleteAllItems()
		pos = 0
		for result in self.results:
			self.insertResult(result, pos)
			pos += 1

	def addResult(self, event):
		result = event.data
		self.results.append(result)
		self.sortList()
		self.insertResult(result, self.results.index(result))
		wxYield()

	def sortList(self):
		if len(self.results) < 2: return
		
		if self.info.sortAlgo == 0:
			return
		elif self.info.sortAlgo == 1:
			self.results.sort(lambda x, y: cmp(x.userNick, y.userNick))
		elif self.info.sortAlgo == -1:
			self.results.sort(lambda x, y: cmp(y.userNick, x.userNick))
		elif self.info.sortAlgo == 2:
			self.results.sort(lambda x, y: cmp(x.path, y.path))
		elif self.info.sortAlgo == -2:
			self.results.sort(lambda x, y: cmp(y.path, x.path))
		elif self.info.sortAlgo == 3:
			self.results.sort(lambda x, y: cmp(x.type, y.type))
		elif self.info.sortAlgo == -3:
			self.results.sort(lambda x, y: cmp(y.type, x.type))
		elif self.info.sortAlgo == 4:
			self.results.sort(lambda x, y: cmp(y.size, x.size))
		elif self.info.sortAlgo == -4:
			self.results.sort(lambda x, y: cmp(x.size, y.size))
		elif self.info.sortAlgo == 5:
			self.results.sort(lambda x, y: y.freeSlots - x.freeSlots)
		elif self.info.sortAlgo == -5:
			self.results.sort(lambda x, y: x.freeSlots - y.freeSlots)
		elif self.info.sortAlgo == 6:
			self.results.sort(lambda x, y: 0)
		elif self.info.sortAlgo == -6:
			self.results.sort(lambda x, y: 0)
		elif self.info.sortAlgo == 7:
			self.results.sort(lambda x, y: cmp(x.hubName, y.hubName))
		elif self.info.sortAlgo == -7:
			self.results.sort(lambda x, y: cmp(y.hubName, x.hubName))

	def insertResult(self, result, pos):
		self.list.InsertStringItem(pos, result.userNick)
		self.list.SetStringItem(pos, 1, basename(result.path))
		self.list.SetStringItem(pos, 2, result.type)
		self.list.SetStringItem(pos, 3, formatSize(result.size))
		self.list.SetStringItem(pos, 4, str(result.freeSlots) + '/' + str(result.slots))
		self.list.SetStringItem(pos, 5, '0')
		self.list.SetStringItem(pos, 6, result.hubName)

class SearchViewerInfo(JobViewerInfo):
	def __init__(self, search):
		JobViewerInfo.__init__(self, search)

		self.pattern = search.getPattern()
		self.insertionPoint = 0
		self.sortAlgo = 0
