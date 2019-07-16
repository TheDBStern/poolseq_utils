#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to convert SNP results into window-based results (average by default)')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'name of output')
parser.add_argument('-p', dest = 'poscol', type = int, required=True,  help = 'column containing position information (base 0)')
parser.add_argument('-r', dest = 'rescol', type = int, required=True,  help = 'column containing statistic of interest (base 0)')
parser.add_argument('--highest', dest = 'highest', action ='store_true', default= False, help ='take the highest SNP value instead of the average')
parser.add_argument('--header', dest = 'header', action ='store_true', default= False, help ='data input has a header line')
parser.add_argument('-w', dest = 'wsize', type = int, required=True,  help = 'genomic window length (non-overlapping)')
parser.add_argument('-u', dest = 'wunit', type = str, required=True,  help = 'genomic window unit("bp" or "snp"))

args = parser.parse_args()

outfile = open(args.output,'w')
outfile.write('Position\tNsnps\tStat\n')

with open(args.input, 'rU') as f:
	if args.header:
		next(f)
	pos0 = 0
	dat = []
	for line in f:
		pos = line.split()[args.poscol]
		if int(pos) < (pos0 + args.wsize):
			dat.append(float(line.split()[args.rescol]))
		else:
			if args.highest:
				out = numpy.max(dat)
			else:
				out = numpy.mean(dat)
			outfile.write('%s\t%s\t%s\n'%(pos0,len(dat),str(out)))
			pos0 = int(pos)
			dat = []

with open(args.input, 'rU') as f:
	if args.header:
		next(f)
	pos0 = 0
	dat = []
	