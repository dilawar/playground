# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os.path
import xml.sax
from xml.dom import minidom
from urlparse import urlparse

from DCUser import *

class DCSettings:
	def __init__(self):
		self.user = DCUser()
		self.download = None
		self.active = 1
		self.hublists = []
		self.share = []
		self.ip = None
		self.port = 412
		self.slots = 3

	def load(self, path):
		try:
			doc = minidom.parse(path)
		except IOError:
			raise ParseError(ParseError.E_IO)
		except xml.sax.SAXParseException:
			raise ParseError(ParseError.E_XML)

		rootElem = doc.documentElement
		if rootElem.nodeName != "settings":
			raise ParseError(ParseError.E_SYNTAX)

		for node in rootElem.childNodes:
			if node.nodeType == node.TEXT_NODE:
				pass

			elif node.nodeName == "nick":
				self.user.nick = self.loadValue(node)

				try:
					pos = self.user.nick.index("|")
					raise ParseError(ParseError.E_RESERVEDCHAR)
				except ValueError: pass

				try:
					pos = self.user.nick.index("$")
					raise ParseError(ParseError.E_RESERVEDCHAR)
				except ValueError: pass

			elif node.nodeName == "connection":
				connection = self.loadValue(node)
				if connection == "56Kbps":
					self.user.connection = DCUser.CONN_56K
				elif connection == "Satellite":
					self.user.connection = DCUser.CONN_SATELLITE
				elif connection == "DSL":
					self.user.connection = DCUser.CONN_DSL
				elif connection == "Cable":
					self.user.connection = DCUser.CONN_CABLE
				elif connection == "LAN(T1)":
					self.user.connection = DCUser.CONN_T1
				elif connection == "LAN(T3)":
					self.user.connection = DCUser.CONN_T3
				else:
					raise ParseError(ParseError.E_UNKNOWNCONNECTION)

			elif node.nodeName == "description":
				if len(node.childNodes) != 0:
					self.user.description = self.loadValue(node)

			elif node.nodeName == "email":
				if len(node.childNodes) != 0:
					self.user.email = self.loadValue(node)

			elif node.nodeName == "download":
				if self.download != None:
					raise ParseError(ParseError.E_SYNTAX)

				download = self.loadValue(node)
				if not os.path.isdir(download):
					raise ParseError(ParseError.E_INVALIDDOWNLOAD)
				self.download = os.path.abspath(download)

			elif node.nodeName == "share":
				for dirNode in node.childNodes:
					if dirNode.nodeName == "dir":
						share = self.loadValue(dirNode)
						if not os.path.isdir(share):
							raise ParseError(ParseError.E_INVALIDSHARE)
						self.share.append(share)
					elif dirNode.nodeType == dirNode.TEXT_NODE:
						pass
					else:
						raise ParseError(ParseError.E_SYNTAX)
						
			elif node.nodeName == "mode":
				value = self.loadValue(node, 0)
				if value == "active":
					self.active = 1
				elif value == "passive":
					self.active = 0
				else:
					raise ParseError(ParseError.E_INVALIDMODE)
					
			elif node.nodeName == "hublist":
				for sourceNode in node.childNodes:
					if sourceNode.nodeName == "source":
						source = self.loadValue(sourceNode)
						i = urlparse(source)
						if i[0] != 'http' or len(i[1]) == 0:
							raise ParseError(ParseError.E_INVALIDHUBLISTSOURCE)
						self.hublists.append(source)
					elif sourceNode.nodeType == sourceNode.TEXT_NODE:
						pass
					else:
						raise ParseError(ParseError.E_SYNTAX)

			elif node.nodeName == "ip":
				#TODO: add consistency check
				self.ip = self.loadValue(node, 0)

			elif node.nodeName == "port":
				try:
					value = self.loadValue(node, 0)
					if value != None:
						port = int(value)
						if port < 1: raise ParseError(ParseError.E_INVALIDPORT)
						self.port = port
				except ValueError:
					raise ParseError(ParseError.E_INVALIDPORT)

			elif node.nodeName == "slots":
				try:
					value = self.loadValue(node, 0)
					if value != None:
						slots = int(value)
						if slots < 0: raise ParseError(ParseError.E_INVALIDSLOTNUM)
						self.slots = slots
				except ValueError:
					raise ParseError(ParseError.E_INVALIDSLOTNUM)

			elif node.nodeName == "sharesize":
				try:
					value = self.loadValue(node, 0)
					if value != None:
						size = long(value)
						if size < 0: raise ParseError(ParseError.E_INVALIDSHARESIZE)
						self.user.share = size
				except ValueError:
					raise ParseError(ParseError.E_INVALIDSHARESIZE)

			else:
				raise ParseError(ParseError.E_SYNTAX)
				
		if self.user.nick == None:
			raise ParseError(ParseError.E_NONICK)
		elif self.user.connection == DCUser.CONN_NONE:
			raise ParseError(ParseError.E_NOCONNECTION)
		elif self.download == None:
			raise ParseError(ParseError.E_NODOWNLOAD)
		elif len(self.share) == 0 and self.user.share == 0L:
			raise ParseError(ParseError.E_INVALIDSHARE)

	def loadValue(self, node, required = 1):
		if len(node.childNodes) != 1:
			if required:
				raise ParseError(ParseError.E_SYNTAX)
			else:
				return None

		valueNode = node.childNodes[0]
		if valueNode.nodeType != node.TEXT_NODE:
			raise ParseError(ParseError.E_SYNTAX)

		return valueNode.nodeValue.encode('ascii')

class ParseError:
	E_IO = 1
	E_XML = 2
	E_SYNTAX = 3
	E_UNKNOWNCONNECTION = 4
	E_RESERVEDCHAR = 5
	E_NONICK = 6
	E_NOCONNECTION = 7
	E_NODOWNLOAD = 8
	E_INVALIDDOWNLOAD = 9
	E_INVALIDSHARE = 10
	E_INVALIDMODE = 11
	E_INVALIDPORT = 12
	E_INVALIDSLOTNUM = 13
	E_INVALIDSHARESIZE = 14
	E_INVALIDHUBLISTSOURCE = 15

	def __init__(self, code):
		self.code = code
		if code == self.E_IO:
			self.description = "read failure"
		elif code == self.E_XML:
			self.description = "malformed XML"
		elif code == self.E_SYNTAX:
			self.description = "wrong syntax"
		elif code == self.E_UNKNOWNCONNECTION:
			self.description = "unknown connection"
		elif code == self.E_RESERVEDCHAR:
			self.description = "character reserved by DC protocol"
		elif code == self.E_NONICK:
			self.description = "no nick found"
		elif code == self.E_NOCONNECTION:
			self.description = "no connection type found"
		elif code == self.E_NODOWNLOAD:
			self.description = "no download location found"
		elif code == self.E_INVALIDDOWNLOAD:
			self.description = "invalid download directory"
		elif code == self.E_INVALIDSHARE:
			self.description = "invalid share directory"
		elif code == self.E_INVALIDMODE:
			self.description = "invalid work mode"
		elif code == self.E_INVALIDPORT:
			self.description = "invalid listening port"
		elif code == self.E_INVALIDSLOTNUM:
			self.description = "invalid slot number"
		elif code == self.E_INVALIDSHARESIZE:
			self.description = "invalid share size"
		elif code == self.E_INVALIDHUBLISTSOURCE:
			self.description = "invalid hublist source"

	def __repr__(self):
		return "Error: " + self.description + "."

	def getDescription(self):
		return self.description
