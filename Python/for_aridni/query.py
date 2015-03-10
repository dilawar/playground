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

db = list()

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
            for q in queris:
                if "V$%s"%q.upper() in uniqueDb:
                    print("[MATCH] %s found" % q)

def main():
    dbFile = sys.argv[1]
    queryFile = sys.argv[2]
    query(queryFile, dbFile)

if __name__ == '__main__':
    main()
