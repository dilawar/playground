# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from wxPython.wx import *
from EventGenerator import *
from JobViewer import *
from JobViewerInfo import *
from Util import *
#DEBUG
import sys

from DCHub import DCHub
import DCWorker

class ChatJob(EventGenerator):
	def __init__(self, nick, hub):
		EventGenerator.__init__(self)
		self.nick = nick
		self.hub = hub
		self.address = hub.getAddress()
		self.rows = []

	def appendMsg(self, msg):
		self.rows.append(msg.replace('\r', ''))

		self.lock.acquire()
		for listener in self.listeners:
			listener.onMsg(self.nick, msg)
		self.lock.release()

	def sendMsg(self, msg):
		if self.address != self.hub.getAddress():
			#TODO: alert user
			return

		self.hub.sendMsg(msg, self.nick)
		self.appendMsg('<%s> %s\n' % (DCWorker.getWorker().getUser().nick, msg))

	def getNick(self):
		return self.nick

	def getAddress(self):
		return self.address

	def getRows(self):
		return self.rows

class ChatJobEventListener:
	def onMsg(nick, msg):
		pass

class ChatViewer(wxPanel, EventGenerator, JobViewer, ChatJobEventListener):
	def __init__(self, parent, id, info):
		wxPanel.__init__(self, parent, id)
		EventGenerator.__init__(self)
		JobViewer.__init__(self, info)
		
		self.text = wxTextCtrl(self, -1, style = wxTE_MULTILINE | wxTE_RICH)
		self.msg = wxTextCtrl(self, 1, style = wxTE_PROCESS_ENTER)
		close = wxButton(self, 2, 'Close')

		hLayout = wxBoxSizer(wxHORIZONTAL)
		hLayout.Add(self.msg, 1, wxEXPAND)

		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.text, 1, wxEXPAND)
		vLayout.Add(hLayout, 0, wxEXPAND | wxBOTTOM | wxTOP, 5)
		vLayout.Add(close, 0, wxALIGN_CENTER | wxBOTTOM | wxTOP, 5)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_TEXT_ENTER(self, 1, self.onSend)
		EVT_BUTTON(self, 2, self.onClose)

		self.text.SetEditable(0)
		for i in self.info.getJob().getRows():
			self.appendRow(i)

		if self.info.msgText != None:
			self.msg.SetValue(self.info.msgText)

	def Destroy(self):
		self.info.msgText = self.msg.GetValue()

		JobViewer.__del__(self)
		return wxPanel.Destroy(self)

	def getTitle(self):
		return self.info.getJob().getNick()

	def onMsg(self, nick, msg):
		#NOTE: this implementation assumes that this
		#      function is executed by main (GUI) thread
		self.appendRow(msg)

	def onSend(self, event):
		text = self.msg.GetValue()
		if len(text) == 0: return

		self.info.getJob().sendMsg(text)
		self.msg.SetValue('')

	def onClose(self, event):
		self.lock.acquire()
		for listener in self.listeners:
			listener.onViewerClosed(self, 1)
		self.lock.release()

		self.Destroy()

	#=================#
	# Private section #
	#=================#

	def appendRow(self, row):
		self.text.AppendText(row)

		lastPos = max(self.text.GetLastPosition() - 1, 0)
		self.text.ShowPosition(lastPos)

		if self.text.GetNumberOfLines() > DCHub.MAX_LOG_ROWS:
			self.text.Remove(0, self.text.GetLineLength(0))

class ChatViewerInfo(JobViewerInfo):
	def __init__(self, chat):
		JobViewerInfo.__init__(self, chat)
		self.msgText = None

