#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/23/20

@author waldo

"""

class AccessRec(object):
    def __init__(self, l):
        self.huid = l[3]
        self.building = l[6]
        self.date = l[1][:-5]
        self.time = l[1][-5:]
        self.who = l[2]
        self.entry = True


class AccessInst(object):
    def __init__(self, access_rec):
        self.who = access_rec.huid
        self.name = access_rec.who
        self.date = access_rec.date
        self.time = access_rec.time
        self.building = access_rec.building

    def csvwrite(self):
        return([self.who, self.name, self.building, self.date, self.time])