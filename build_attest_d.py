#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/29/20

@author waldo


"""
import sys, csv, pickle
import interval_rec as ir
import utilities as ut

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python build_attest_d.py attest_file_in.csv dictionary_file_out.pkl")
        sys.exit(1)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    h = next(cin)

    att_d = {}
    for l in cin:
        v = ir.TimeInterval(l)
        huid = l[0]
        att_d[huid] = att_d.setdefault(huid, [])
        att_d[huid].append(v)

    fin.close()

    ut.write_pickle(sys.argv[2], att_d)

