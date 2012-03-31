# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCQueueEventListener:
    def onNewItem(self, queue, item):
        pass

    def onItemRemoved(self, queue, item):
        pass

    def onItemStatus(self, queue, item):
        pass

