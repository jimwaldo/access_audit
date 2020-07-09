#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/25/20

@author waldo

A program that takes as input a file containing the access logs as sent to SEAS and FAS Science, and extracts those
access that are at the periphery (determined by looking at the name of the card unit and seeing if it contains either
"Entry" or "Exterior") and checks to see if those who are entering are on the allowed list supplied by the Deans.

The program will filter out custodians and security people. It will also filter out hourly and part-time tradespeople.

The program assumes that a pickle file containing a dictionary from huid->employee records (as defined in
employee_rec.py) and a pickle file containing the set of HUIDs that are allowed into the buildings are in the same
directory in which the program is run; these need to be called uid_dict.pkl and allowed_set.pkl, respectively.

The program produces three files:

SuspectAccess.csv, a listing of the huid, name, building, data and time of access for those accessing the building who
are not on the authorized access list

AllowedAccess.csv, a listing like the above but of those who are on the authorized access list

BuildingAccess.csv, a listing of each building accessed and the number of times it was accessed

Each of these can be read into a spreadsheet, which allows sorting and visual displays of various kinds.
"""

import access_rec as ar
import pickle, csv, sys

uid_fname = 'uid_dict.pkl'
allow_set_fname = 'allowed_set.pkl'
grey_set_fname = 'grey_set.pkl'


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


def write_accessfile(fname, access_l):
    """
    Writes an output file, showing who has accessed one of the buildings in the input set of door records. The files
    all have the same format, but there will be one for those who have been allowed access, another for those whose
    job requires access, and a third for those who should not be entering the buildings
    :param fname: Name of the file to write
    :param access_l: A list of AccessRec objects  for those who have accessed the buildings, along with the building
    accessed, the date, and the
    time of access
    :return: None
    """
    fout = open(fname, 'w')
    cout = csv.writer(fout)
    cout.writerow(['HUID', 'Name', 'Building', 'Date', 'Time'])
    for a in access_l:
        cout.writerow(a.csvwrite())
    fout.close()
    return


def write_building_file(fname, building_d):
    """
    Write a file with the total number of building accesses, by building, from a particular list. This allows a quick
    check to see what buildings are seeing the most traffic
    :param fname: Name of the file to write the access records
    :param building_d: A dictionary, keyed by building name, with values the count of the number of access to the building
    :return: None
    """
    build_l = []
    for k, v in building_d.items():
        build_l.append([k, v])
    build_l.sort()

    fout = open(fname, 'w')
    cout = csv.writer(fout)
    cout.writerow(['building', 'Total Accessed'])
    cout.writerows(build_l)
    fout.close()
    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python process_access_list access_list.csv')
        sys.exit(1)

    # read in the uid->employee_rec dictionary, and the access_set
    uid_dict = read_pickle(uid_fname)
    approved_set = read_pickle(allow_set_fname)
    grey_set = read_pickle(grey_set_fname)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    h = next(cin)

    build_access_d = {}
    r_building_access_d = {}
    access_suspect = []
    access_allowed = []
    access_grey = []

    for l in cin:
        access = ar.AccessRec(l)
        huid = access.huid
        if huid not in grey_set:
            r_building_access_d[access.building] = r_building_access_d.setdefault(access.building, 0) + 1
        build_access_d[access.building] = build_access_d.setdefault(access.building, 0) + 1
        if huid in approved_set:
            access_allowed.append(access)
        elif huid in grey_set:
            access_grey.append(access)
        else:
            access_suspect.append(access)

    write_accessfile('SuspectAccess.csv', access_suspect)
    write_accessfile('AllowedAccess.csv', access_allowed)
    write_accessfile('GreyAccess.csv', access_grey)
    write_building_file('BuildingAccess.csv', build_access_d)
    write_building_file('ResearcherBuildingAccess.csv', r_building_access_d)
