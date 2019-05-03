#!/usr/bin/env python
from __future__ import division
import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to convert a file from multipopulation BayPass format (Scaffold position refcount1 altcount1 etc.) to NCD format. Splits by chromosome and population')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-n', dest = 'numPops', type = int, required=True,  help = 'number of populations')

## Format: CHR   POS      ID REF ALT       AF1        AF2      AF3        MAF

args = parser.parse_args()

for i in range(1,args.numPops+1):
	os.mkdir('pop'+str(i))

with open(args.input,'rU') as f:
	for line in f:
		pcount = 1
		scaf = line.split(' ')[0]
		scafnum = scaf.strip('Scaffold')
		pos = line.split(' ')[1]
		ID = scafnum+'|'+pos
		for pop in range(0,args.numPops*2,2):
			output = open('pop'+str(pcount)+'/'+str(scaf), 'a')
			c1 = int(line.split(' ')[pop+2]) # get first allele count for each pop
			c2 = int(line.split(' ')[pop+3]) # second allele count
			tot = c1 + c2
			AF1 = round(c1/tot,4)
			AF2 = round(c2/tot,4)
			AF3 = "NA"
			MAF = min(AF1,AF2)
			output.write(str(scafnum)+'\t'+str(pos)+'\t'+str(ID)+'\t'+str(AF1)+'\t'+str(AF2)+'\t'+str(AF3)+'\t'+str(MAF)+'\n')
			pcount +=1