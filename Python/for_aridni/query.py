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
conditions = defaultdict()


def query(qFile, dbFile, conditionFile):
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

    with open(conditionFile, "r") as condF:
        cond = csv.reader(condF, dialect='excel')
        for row in cond:
            genes = row[0].split(',')
            for gene in genes:
                conditions[gene] = row[1:]
                #newRows.append([gene] + row[1:])


    with open('match.csv', 'w') as outF:
        outF.write("query,results\n")
        for k in found:
            # Check condition
            newFound = checkCondition(k)
            print newFound
            if newFound:
                outF.write(k+",")
                outF.write(",".join(newFound))
                outF.write("\n")

def checkCondition(gene):
    print("Checking for %s" % gene)
    founds = found[gene]
    newFound = []
    for f in founds:
        c = conditions.get(f.upper(), [])
        if not c:
            newFound.append(f)
        else:
            control, treatment, foldChange = [float(x) for x in c]
            if control > 0.5 or treatment > 0.5:
                if foldChange > 1.5 or foldChange < -0.6:
                    newFound.append(f)
    return newFound


def main():
    dbFile = sys.argv[1]
    queryFile = sys.argv[2]
    conditionFile = sys.argv[3]
    query(queryFile, dbFile, conditionFile)

if __name__ == '__main__':
    main()
