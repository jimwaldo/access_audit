#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 5/29/2020

@author waldo

A collection of handy routines that get used in multiple other programs
"""
import pickle
import datetime as dt


def read_pickle(fname):
    """
    Read the object stored in the named file. Opens the file, reads the pickle, and returns the object after closing
    the file
    :param fname: name of the file containing the pickle. It is assumed that the structure of the pickle is known
    to the caller
    :return: The object that was pickled in the named file
    """
    fin = open(fname, 'rb')
    ret_val = pickle.load(fin)
    fin.close()
    return ret_val

def write_pickle(fname, to_pickle):
    fout = open(fname, 'wb')
    pickle.dump(to_pickle, fout)
    fout.close()
    return None

def d_str_to_date(d_s):
    m = int(d_s[:2])
    d = int(d_s[2:4])
    y = int(d_s[-4:])
    return dt.date(y, m, d)

def t_str_to_time(t_s):
    h = int(t_s[:2])
    m = int(t_s[-2:])
    return dt.time(h, m)

