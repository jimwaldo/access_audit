#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/23/20

@author waldo

Definition of the class that will be used to represent information on all HUID holders. This will be used to
cross-reference those who go in to buildings with those who are allowed, either because of their job (security,
custodians) or because they have been authorized by the deans.

Note that as of 3/12, this object is no longer required, as the system works around three sets of files specifying
HUID and entry status, which means that this could be removed. However, as things may change in the future, we will
keep this for now.
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
        """
        Can be called to see if the employee should be excluded from listing. Originally this was to be used to keep
        from listing custodians, security, and trades people. These have now been added to the
        :param class_exclude_s: A set of HUIDs to exclude from reports
        :return: True if the employee is to be excluded from the reports, false otherwise
        """
        ex_status= False
        if ('Custod' in self.role) or ('Security' in self.role):
            return True
        if self.emp_class in class_exclude_s:
            ex_status = True
        return ex_status

    def check_permitted(self, permitted_s):
        """
        Checks to see if the employee is on the permitted set handed in as a parameter
        :param permitted_s: A set of those permitted to have access
        :return: True if the employee is in the set, and False otherwise
        """
        if self.huid in permitted_s:
            return True
        else:
            return False

