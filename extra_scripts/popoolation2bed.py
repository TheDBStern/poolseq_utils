#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='This script takes the output of a window-based popoolation analysis and turns it into a bed file with the start and end of the window')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'output file name; bed format')
parser.add_argument('-w', dest = 'wsize', type = float, required=True,  help = 'window size used to calculate the statistic of interest')
args = parser.parse_args()

outfile = open(args.output,'w')

with open(args.input, 'rU') as f:
	for line in f:
		scaf = line.split('\t')[0]
		mid = float(line.split('\t')[1])
		dat = '\t'.join(line.split('\t')[2:])
		start = int(mid - (args.wsize / 2))
		end = int(mid + (args.wsize / 2))
		outfile.write('%s\t%s\t%s\t%s'%(scaf,str(start),str(end),dat))