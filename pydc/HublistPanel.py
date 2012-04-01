# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from Util import *
from wx import *
import sys

from DCHublistRetriever import *
from DCHublistRetrieverEventListener import *
import DCWorker

class HublistPanel(wxPanel, DCHublistRetrieverEventListener):
	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)

		self.sortAlgos = [ None,
		                   (self.getHubName, cmp),
		                   (self.getHubAddress, cmp),
		                   (self.getHubDescription, cmp),
		                   (self.getHubUserNum, icmp),

		                   (self.getHubUserNum, cmp),
		                   (self.getHubDescription, icmp),
		                   (self.getHubAddress, icmp),
		                   (self.getHubName, icmp) ]
		self.sortAlgo = 4
		self.hubList = []

		self.refresh = wxButton(self, 1, "Refresh")
		self.list = wxListCtrl(self, 2, style = wxLC_REPORT | wxLC_VRULES)
		self.connect = wxButton(self, 3, "Connect")
		self.text = wxTextCtrl(self, 4, style = wxTE_PROCESS_ENTER)

		self.list.InsertColumn(0, "Name")
		self.list.InsertColumn(1, "Address")
		self.list.InsertColumn(2, "Description")
		self.list.InsertColumn(3, "Users", wxLIST_FORMAT_RIGHT)
		
		vLayout = wxBoxSizer(wxVERTICAL)
		hLayout = wxBoxSizer(wxHORIZONTAL)

		hLayout.Add(self.connect)
		hLayout.Add(self.text, 1, wxLEFT | wxEXPAND, 2)
		vLayout.Add(self.refresh, 0, wxEXPAND | wxTOP, 5)
		vLayout.Add(self.list, 1, wxEXPAND | wxTOP, 5)
		vLayout.Add(hLayout, 0, wxEXPAND | wxTOP, 5)
		
		self.SetSizer(vLayout)
		self.Layout()
		
		EVT_BUTTON(self, 1, self.onRefresh)
		EVT_LIST_COL_CLICK(self, 2, self.setSortAlgo)
		EVT_LIST_ITEM_ACTIVATED(self, 2, self.onListConnect)
		EVT_BUTTON(self, 3, self.onManualConnect)
		EVT_TEXT_ENTER(self, 4, self.onManualConnect)
		self.Connect(1, 1, wxEVT_NULL, self.displayList)
		self.Connect(2, 2, wxEVT_NULL, self.displayError)

	def onRefresh(self, event):
		retriever = DCHublistRetriever()
		retriever.registerListener(self)
		DCWorker.getWorker().addJob(retriever)
		
	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		access, comp = self.sortAlgos[self.sortAlgo]
		self.hubList = fullSort(self.hubList, access, comp)
		self.updateList()
		
	def onListConnect(self, event):
		getMainWnd().connectToHub(self.hubList[event.GetIndex()][1])

	def onManualConnect(self, event):
		addr = self.text.GetValue()
		if addr != '':
			self.text.SetValue('')
			getMainWnd().connectToHub(addr)
		else:
			first = 1
			for i in range(0, self.list.GetItemCount()-1):
				if self.list.GetItemState(i, wxLIST_MASK_STATE):
					if first:
						getMainWnd().connectToHub(self.hubList[i][1])
						first = 0
					else:
						getMainWnd().connectToHub(self.hubList[i][1], 0)
		
	def onHublist(self, list):
		if list == None or len(list) == 0:
			if len(self.hubList) == 0:
				wxPostEvent(self, wxPyEvent(2))
		else:
			wxPostEvent(self, guiEvent(1, list))
				
	def displayList(self, event):
		self.hubList = sys.modules['__main__'].hublist = event.data

		access, comp = self.sortAlgos[self.sortAlgo]
		self.hubList = fullSort(self.hubList, access, comp)
		self.updateList()
		
	def displayError(self, event):
		self.list.DeleteAllItems()
		self.list.InsertStringItem(0, 'Error...')
		
	#=================#
	# Private section #
	#=================#

	def getHubName(self, item):
		return item[0].lower()

	def getHubAddress(self, item):
		return item[1]

	def getHubDescription(self, item):
		return item[2].lower()

	def getHubUserNum(self, item):
		return item[3]

	def updateList(self):
		if len(self.hubList) == 0: return

		self.list.Freeze()
		self.list.DeleteAllItems()
		pos = 0
		for i in self.hubList:
			self.list.InsertStringItem(pos, i[0])
			self.list.SetStringItem(pos, 1, i[1])
			self.list.SetStringItem(pos, 2, i[2])
			self.list.SetStringItem(pos, 3, str(i[3]))
			pos += 1
		self.list.Thaw()
