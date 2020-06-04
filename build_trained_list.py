#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 6/1/20

@author waldo

Take a .csv file obtained from the Harvard Training Portal of HUIDs that have passed the COVID return training and
create a set of those HUIDs. This may need to be changed if the format of the file is different than a simple list
of HUIDs
"""

import sys, csv, utilities

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python build_trained_set.py input_file.csv")
        sys.exit(1)

    huid_s = set()
    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    for l in cin:
        if l[0].isdigit():
            huid_s.add(l[0])
    fin.close()
    utilities.write_pickle('trained_set.pkl', huid_s)
