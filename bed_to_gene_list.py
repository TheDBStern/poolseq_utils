#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to get blast result names from bedfile with gene names')
parser.add_argument('-bed', dest = 'bed', type = str, required=True,  help = 'bedfile input file')
parser.add_argument('-blast', dest = 'blast', type = str, required=True,  help = 'blast file input; outfmt 6')
parser.add_argument('-o', dest = 'out', type = str, required=True,  help = 'output file')

args = parser.parse_args()

outfile = open(args.out,'w')

with open(args.bed,'rU') as f:
	for line in f:
		b = open(args.blast,'rU')
		dat = line.split('\t')[0:5]
		info = line.split('\t')[8]
		id = info.split(';')[0]
		gene = id.strip('ID=')
		out = '%s\t%s\n'%('\t'.join(dat),id)
		for l in b:
			geneid = l.split('\t')[0].strip('-PA')
			geneinfo = l.split('\t')[1]
			if gene in geneid:
				out = '%s\t%s\t%s\n'%('\t'.join(dat),id,geneinfo)
		outfile.write(out)