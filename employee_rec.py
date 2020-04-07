#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/23/20

@author waldo

Definition of the class that will be used to represent information on all HUID holders. This will be used to
cross-reference those who go in to buildings with those who are allowed, either because of their job (security,
custodians) or because they have been authorized by the deans
"""
import sys, csv, pickle

class EmpRec(object):
    def __init__(self, l):
        self.huid = l[0]
        self.first_name = l[2]
        self.last_name = l[3]
        self.email = l[1]
        self.emp_class = l[8]
        self.role = l[9]

    def check_exclude(self, class_exclude_s):
        ex_status= False
        if ('Custod' in self.role) or ('Security' in self.role):
            return True
        if self.emp_class in class_exclude_s:
            ex_status = True
        return ex_status

    def check_permitted(self, permitted_s):
        if self.huid in permitted_s:
            return True
        else:
            return False

