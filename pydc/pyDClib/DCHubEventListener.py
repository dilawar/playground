# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCHubEventListener:
    def onLogUpdate(self, hub, row):
        pass

    def onHubInfo(self, hub):
        pass

    def onHubDisconnection(self, hub):
        pass

    def onNewUser(self, hub, user):
        pass

    def onUserDisconnection(self, hub, user):
        pass
    
    def onUserInfo(self, hub, user):
        pass
