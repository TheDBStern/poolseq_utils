#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to calculate the window PBE statistic for three populations of interest from the output of popoolation2s Fst calculation')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file of pairwise Fst')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'output file name')
parser.add_argument('-F', dest = 'foc', type = str, required=True,  help = 'number of the focal population based on its position in the population calculation')
parser.add_argument('-NF1', dest = 'nfoc1', type = str, required=True,  help = 'number of the first non-focal population')
parser.add_argument('-NF2', dest = 'nfoc2', type = str, required=True,  help = 'number of the second non-focal population')

args = parser.parse_args()

outfile = open(args.output,'w')

nf_pops = {args.nfoc1,args.nfoc2}
comp1 = {args.nfoc1,args.foc}
comp2 = {args.foc,args.nfoc2}

def calc_PBS_Tbc(dats):
	nf_fst = 0
	foc_fst1 = 0
	foc_fst2 = 0
	for dat in dats:
		fst = float(dat.split('=')[1])
		pops = {dat.split('=')[0].split(':')[0],dat.split('=')[0].split(':')[1]}
		if pops == nf_pops:
			nf_fst += fst
		elif pops == comp1:
			foc_fst1 += fst
		elif pops == comp2:
			foc_fst2 += fst
	PBS = (-(numpy.log(1-foc_fst1)) + -(numpy.log(1-foc_fst2)) - -(numpy.log(1-nf_fst))) / 2
	Tbc = -(numpy.log10(1 - nf_fst))
	return(PBS,Tbc)
	
def calc_PBE(PBS,Tbc,PBS_med,Tbc_med):
	PBE = PBS - (Tbc * (PBS_med / Tbc_med))
	return(PBE)

all_PBS = []
all_Tbc = []
results = {}
with open(args.input, 'rU') as f:
	for line in f:
		loc = '\t'.join(line.split('\t')[0:2])
		res = calc_PBS_Tbc(line.split('\t')[5:])
		all_PBS.append(res[0])
		all_Tbc.append(res[1])
		results[loc]=res


for loc in sorted(results.iterkeys()):
	PBE = calc_PBE(results[loc][0],results[loc][1],numpy.median(all_PBS),numpy.median(all_Tbc))
	outfile.write(loc+'\t'+str(PBE)+'\n')
