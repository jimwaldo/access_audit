#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/26/20

@author waldo

"""
import csv, pickle, sys
import employee_rec as er


def load_uid_dict(fname):
    fin = open(fname, 'rb')
    d_out = pickle.load(fin)
    fin.close()
    return d_out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python employee_rec.py huid_list.csv output_dict.pkl")
        exit(1)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    h = next(cin)
    e_d = {}

    for l in cin:
        if l[0] not in e_d:
            e_d[l[0]] = er.EmpRec(l)

    fout = open(sys.argv[2], 'wb')
    pickle.dump(e_d, fout)
    fin.close()
    fout.close()

