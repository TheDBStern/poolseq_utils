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
		if len(line.split('\t')) < 7:
			pass
		else:
			b = open(args.blast,'rU')
			dat = line.split('\t')[0:3]
			gene = line.split('\t')[8]
			dist = line.split('\t')[14].split('|')[1].strip('\n')
			out = '%s\t%s\n'%('\t'.join(dat),gene)
			for l in b:
				geneid = l.split('\t')[0].strip('-PA')
				geneinfo = l.split('\t')[1]
				if gene in geneid:
					out = '%s\t%s\t%s\t%s\n'%('\t'.join(dat),gene,geneinfo,dist)
			outfile.write(out)