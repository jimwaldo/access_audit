#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/25/20

@author waldo

A program that takes as input a file containing the access logs as sent to SEAS and FAS Science, and extracts those
accesses and checks to see if those who are entering have taken the required training and have
self-attested to having no COVID-19 symptoms.

The program assumes that a csv file containing a dictionary from huid->interval records (as defined in
interval_rec.py) for those who have self-attested to no symptoms, and a csv file containing the set of HUIDs that have
completed training that allows return to campus. These need to be in filescalled attest_d.csv and trained_set.csv,
respectively.

The program produces three files:

SuspectAccess.csv, a listing of the huid, name, building, data and time of access, and whether or not they have taken
 training, for those accessing the building who are not on the authorized for access.

AllowedAccess.csv, a listing like the above but of those who are authorized for the access

BuildingAccess.csv, a listing of each building accessed and the number of times it was accessed

Each of these can be read into a spreadsheet, which allows sorting and visual displays of various kinds.

There is also an option to have a file called grey_set.pkl, a pickle file for a set of HUIDs. The HUIDs in this set will
be seen as allowed, but will be written out in a file called grey_access.csv. This allows exclusion of arbitrary
persons from the requirements of the training and self-attestation.
"""

import access_rec as ar
import interval_rec as ir
import csv, sys, os

from utilities import read_pickle

attest_fname = 'attest_d.csv'
trained_set_fname = 'trained_set.csv'
tested_set_fname = 'tested_set.csv'
grey_set_fname = 'grey_set.pkl'
allowed_set_fname = 'allowed_set.pkl'


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
    cout.writerow(['HUID', 'Name', 'Building', 'Trained', 'Allowed', 'Tested', 'Cleared', 'Date', 'Time'])
    for a in access_l:
        cout.writerow(a.csvwrite_trained_permitted_tested())
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


def make_attest_d():
    """
    Create and return a dictionary keyed by HUID with values a list of a pair of datetime objects, which represent the
    interval of time that the person with the key HUID is allowed to enter buildings based on self-attested lack of
    COVID-19 symptoms. The data for the dictionary is stored in a csv file with the name stored in the global
    attest_fname. The value is a list, as the person may self-attest multiple times.
    :return: a dictionary keyed by HUID with values a list of pairs of datetime objects representing the interval of
    time the person is allowed to enter buildings
    """
    fin = open(attest_fname, 'r')
    cin = csv.reader(fin)
    ret_d = {}
    for l in cin:
        if l[0].isdigit():
            v = ir.TimeInterval(l)
            huid = l[0]
            ret_d[huid] = ret_d.setdefault(huid, [])
            ret_d[huid].append(v)
    fin.close()
    return ret_d


def make_qual_set(fname):
    """
    Create a set of HUIDs for the people who have taken the mandated return-to-campus training. This comes from a file
    supplied daily by the Harvard training people, which is a csv file containing one HUID per line. The file must be
    given the name corresponding to the global variable trained_set_fname.
    :return: A set of HUIDs representing those who have taken the mandated training
    """
    fin = open(fname, 'r')
    cin = csv.reader(fin)
    ret_s = set()
    for l in cin:
        if l[0].isdigit():
            ret_s.add(l[0])
    fin.close()
    return ret_s


def check_access_t(access_d, acc):
    """
    Checks to see if the person accessing a building had self-attested and had permission to access the building at the
    time of access
    :param access_d: the dictionary keyed by HUID with value the list of intervals of times authorized; this is the
    dictionary produced by make_attest_d
    :param acc: an access record taken from the building access logs, in access_rec form
    :return: True if the access occurred during a period of authorized access, False otherwise
    """
    if acc.huid not in access_d:
        return False
    allow_l = access_d[acc.huid]
    for i in allow_l:
        if i.check_interval(acc.datetime):
            return True

    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python process_access_list access_list.csv')
        sys.exit(1)

    # read in the uid->employee_rec dictionary, and the access_set
    if os.path.exists(attest_fname):
        attest_dict = make_attest_d()
    else:
        print(attest_fname, "not in directory; program exiting")
        sys.exit(1)
    if os.path.exists(trained_set_fname):
        trained_set = make_qual_set(trained_set_fname)
    else:
        print(trained_set_fname, "not in directory, program exiting")
        sys.exit(1)
    if os.path.exists(tested_set_fname):
        tested_set = make_qual_set(tested_set_fname)
    else:
        print(tested_set_fname, 'not in directory, empty test set will be used')
        tested_set = set()
    if os.path.exists(grey_set_fname):
        grey_set = read_pickle(grey_set_fname)
    else:
        print(grey_set_fname, "Not in directory, empty grey set will be used")
        grey_set = set()
    if os.path.exists(allowed_set_fname):
        allowed_set = read_pickle(allowed_set_fname)
    else:
        print(allowed_set_fname, "not in directory, empty allowed set will be used")
        allowed_set = set()

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    h = next(cin)

    build_access_d = {}
    r_build_access_d = {}
    access_suspect = []
    access_allowed = []
    access_grey = []
    seen_set = set()

    for l in cin:
        access = ar.AccessRec(l)
        huid = access.huid
        bldg = access.building
        if (huid, bldg) not in seen_set:
            seen_set.add((huid, bldg))
            build_access_d[bldg] = build_access_d.setdefault(bldg, 0) + 1
            if huid not in grey_set:
                r_build_access_d[bldg] = r_build_access_d.setdefault(bldg, 0) + 1
        if huid in trained_set:
            access.trained = True
        if huid in allowed_set:
            access.permitted = True
        if huid in tested_set:
            access.tested = True
        access.attested = check_access_t(attest_dict, access)
        if huid in grey_set:
            access_grey.append(access)
        elif access.trained and access.permitted and access.attested:
            access_allowed.append(access)
        else:
            access_suspect.append(access)

    write_accessfile('SuspectAccess.csv', access_suspect)
    write_accessfile('AllowedAccess.csv', access_allowed)
    if len(access_grey) > 0:
        write_accessfile('GreyAccess.csv', access_grey)
    write_building_file('BuildingAccess.csv', build_access_d)
    write_building_file('ResearchBuildingAccess.csv', r_build_access_d)
