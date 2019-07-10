#!/usr/bin/env python
from __future__ import division
import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to convert a file from multipopulation BayPass format (refcount1 altcount1 etc.) to frequencies of the ref allele')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'output file')
parser.add_argument('-n', dest = 'numPops', type = int, required=True,  help = 'number of populations')
parser.add_argument('-fold', dest= 'fold', action ='store_true', default= False, help ='Calculate MAF for each SNP in each pop instead of ref allele frequency, default = False.')


args = parser.parse_args()

outfile = open(args.output,"w")

with open(args.input,'rU') as f:
	for line in f:
		pcount = 1
		freqs = []
		for pop in range(0,args.numPops*2,2):
			c1 = int(line.split(' ')[pop]) # get first allele count for each pop
			c2 = int(line.split(' ')[pop+1]) # second allele count
			tot = c1 + c2
			if args.fold:
				freq = round(min(c1,c2)/tot,3)
			else:
				freq = round(c1/tot,3)
			freqs.append(str(freq))
			pcount +=1
		outfile.write(' '.join(freqs)+'\n')