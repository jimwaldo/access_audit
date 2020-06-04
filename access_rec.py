#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 3/23/20

@author waldo

A class used to report on access to buildings at Harvard. The AccessRec object holds information about a single
access, as reported by a line from the door access list provided by facilities.

"""

import dateutil.parser as dp
import pytz

class AccessRec(object):
    """
    Object used to encapsulate the record of an access to a building. Includes the HUID of the person accessing,
    the building, and the date and time of access (as a datetime.datetime object), along with the name of the person
    and a field indicating whether the person has gone through the required COVID training
    """
    def __init__(self, l):
        tz = pytz.timezone('EST5EDT')
        self.huid = l[3]
        self.building = l[6]
        lt = dp.parse(l[1])
        self.datetime = tz.localize(lt)
        self.who = l[2]
        self.trained = False

    def csvwrite(self):
        """
        Builds a list for the reports generated by process_access_list.py. The returned list will be a single line
        in an output .csv file
        :return: Information from the object in the order needed for the output .csv file
        """
        return([self.huid, self.who, self.building,
                '/'.join([str(self.datetime.month), str(self.datetime.day), str(self.datetime.year)]),
                ':'.join([str(self.datetime.hour), str(self.datetime.minute)])])

    def csvwrite_trained(self):
        return ([self.huid, self.who, self.building, self.trained,
                 '/'.join([str(self.datetime.month), str(self.datetime.day), str(self.datetime.year)]),
                 ':'.join([str(self.datetime.hour), str(self.datetime.minute)])])