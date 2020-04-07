#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 3/23/20

@author waldo

"""
import csv, pickle, sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python allow_list.py allow_sheet.csv {allow_set.pkl}')
        sys.exit(1)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    alllowed_set = set()
    missing_list = []

    h = next(cin)
    l = next(cin)
    while True:
        if len(l) > 3 and l[3] != '':
            alllowed_set.add((l[3]))
        try:
            l = next(cin)
        except StopIteration:
            break
        except:
            continue

    fin.close()
    if len(sys.argv) < 3:
        fout_name = 'allowed_set.pkl'
    else:
        fout_name = sys.argv[2]
    fout = open(fout_name, 'wb')
    pickle.dump(alllowed_set, fout)
    fout.close()
    if len(missing_list) > 0:
        fout = open('Missing_HUIDs.csv', 'w')
        cout = csv.writer(fout)
        cout.writerow(['Name without HUID', 'HUID'])
        cout.writerows(missing_list)
        fout.close()
