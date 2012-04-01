# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCUser:
	CONN_NONE = -1
	CONN_56K = 0
	CONN_SATELLITE = 1
	CONN_DSL = 2
	CONN_CABLE = 3
	CONN_T1 = 4
	CONN_T3 = 5
	
	def __init__(self):
		self.op = 0
		self.nick = None
		self.share = long(-1)
		self.description = None
		self.connection = self.CONN_NONE
		self.email = None
		self.hub = None

	def isOp(self):
		return self.op

	def getNick(self):
		return self.nick

	def getShare(self):
		return self.share

	def getDescription(self):
		return self.description

	def getConnection(self):
		return self.connection

	def getEmail(self):
		return self.email

	def getHub(self):
		return self.hub
		
	def __str__(self):
		s  = "=== DCUser ===\n"
		s += "Op: " + `self.op` + "\n"
		s += "Nick: " + self.nick + "\n"
		s += "Share: " + `self.share` + "\n"
		s += "Description: "
		if self.description != None: s + self.description
		s += "\n"
		s += "Connection: " + `self.connection` + "\n"
		s += "Email: "
		if self.email != None: s = s + self.email
		s += "\n"
		s += "Hub: "
		if self.hub != None: s = s + self.hub.getName()
		
		return s
