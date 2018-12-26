#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='This script takes a list of significant SNP locations and converts it to a bed file of regions of interest. One can specify the window size and number of significant SNPs requires to be in the window. Overlapping windows are combined.')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file of the format CHR\tPosition. MUST BE SORTED BY POSITION')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'output file name; bed format')
parser.add_argument('-w', dest = 'wsize', type = int, required=True,  help = 'total window size, meaning significant SNP will be in the middle of the window')
parser.add_argument('-n', dest = 'nsnp', type = int, required=True,  help = 'number of significant SNPs required for the window to be retained')

args = parser.parse_args()

outfile = open(args.output,'w')

with open(args.input, 'rU') as f:
	cur_win = [] #Chromosome, start, end, snp_num
	count = 1
	for line in f:
		snp_pos = int(line.split('\t')[1])
		if snp_pos - args.wsize / 2 < 0:  #If window overlaps with the start of the chromosome, make window start from 0
			start = 0
			end = args.wsize
		else:
			start = snp_pos - int(args.wsize / 2)
			end = snp_pos + int(args.wsize / 2)
		if cur_win == []:  # Just to account for the first line
			cur_win = [line.split('\t')[0],start,end, 1]
		else:
			if start < cur_win[2] and line.split('\t')[0] == cur_win[0]: # If overlap and on same chromosome
				cur_win[2] = end
				cur_win[3] += 1
			else:
				if cur_win[3] >= args.nsnp:  # If no overlap and current window has greater than the minimum number of significant SNPs, write it out 
					length = cur_win[2] - cur_win[1]
					outfile.write('%s\t%s\t%s\tRegion%s\t%s\t%s\n'%(cur_win[0],cur_win[1],cur_win[2],count,length,cur_win[3]))
					count += 1
					cur_win = [line.split('\t')[0],start,end, 1]
				else: # If no overlap and not enough SNPs in last window, this becomes current window
					cur_win = [line.split('\t')[0],start,end, 1]