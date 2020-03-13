#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to get blast result names from bedfile with gene names')
parser.add_argument('-genes', dest = 'genes', type = str, required=True,  help = 'gene list file file')
parser.add_argument('-blast', dest = 'blast', type = str, required=True,  help = 'blast file input; outfmt 6')
parser.add_argument('-o', dest = 'out', type = str, required=True,  help = 'output file')

args = parser.parse_args()

outfile = open(args.out,'w')

with open(args.genes,'rU') as f:
	for line in f:
		b = open(args.blast,'rU')
		gene = line.strip('\n')
		for l in b:
			geneid = l.split('\t')[0].strip('-PA')
			geneinfo = l.split('\t')[1]
			if gene in geneid:
				out = '%s\t%s\n'%(gene,geneinfo)
		outfile.write(out)