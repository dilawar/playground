# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class Job:
    def poll(self):
        return 1

    def stop(self):
        pass
    
    def isAlive(self):
        return 0
