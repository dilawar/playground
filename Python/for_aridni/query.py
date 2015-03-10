"""query.py: 

    Searches each row of query sheet in columns of database sheet.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import re
import os
import sys
import csv
from collections import defaultdict 

db = list()
found = defaultdict(set)


def query(qFile, dbFile):
    with open(dbFile, "r") as dbF:
        print("[INFO] Opening db file %s" % dbFile)
        for i, line in enumerate(dbF):
            if i == 0: continue
            for e in line.split(','):
                db.append(e.strip())
    uniqueDb = set(db)
    with open(qFile, "r") as qF:
        print("[INFO] Reading queries")
        for i, row in enumerate(qF):
            if i == 0: continue
            queris = row.split(',')
            for qu in queris:
                q = qu[0:3]
                for s in uniqueDb:
                    if not q: continue
                    if q.upper() in s[0:3]:
                        print("For query %s, %s found" % (qu, s))
                        found[q].add(s)

    with open('match.csv', 'w') as outF:
        outF.write("query,results\n")
        for k in found:
            outF.write(k+",")
            outF.write(",".join(found[k]))
            outF.write("\n")

def main():
    dbFile = sys.argv[1]
    queryFile = sys.argv[2]
    query(queryFile, dbFile)

if __name__ == '__main__':
    main()
