#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 5/28/2020

@author waldo

A class used to track the interval of time for those allowed access through the crimson clear application

"""
import dateutil.parser as dp


class TimeInterval(object):
    def __init__(self, l):
        """
        Initialize the class-- this creates an interval that has a start and end time, each of which are datetime
        objects.
        :param l: A line from the crimson-clear feed, made up of three entries-- the huid of the person cleared,
        a start time, and an end time, currently represented as YYYY-MM-DD HH:MM:SS.MS+timezone offste
        """
        self.start_d = dp.parse(l[1])
        self.end_d = dp.parse(l[2])

    def check_interval(self, entry_d):
        """
        Check to see if the passed-in time is within the interval described by this interval. The check is inclusive, so
        even passing in the start or end time will result in returning True
        :arg a datetime object representing a particular time.
        :return True if the time is within the interval; False otherwise
        """
        if self.start_d <= entry_d and entry_d <= self.end_d:
            return True
        else:
            return False