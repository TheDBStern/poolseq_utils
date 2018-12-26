#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy
from itertools import izip


parser = argparse.ArgumentParser(description='Script to filter snps that have a MAF below some threshold in one group (right now works for two groups)')
parser.add_argument('-gfile', dest = 'gfile', type = str, required=True,  help = 'input genobaypass file')
parser.add_argument('-snpdet', dest = 'snpdet', type = str, required=True,  help = 'input snpdet file')
parser.add_argument('-g1', dest = 'g1', type = int, required=True,  help = 'number of pops in group 1 (assuming from the start)')
parser.add_argument('-g2', dest = 'g2', type = int, required=True,  help = 'number of pops in group 2 (assuming the last ones)')
parser.add_argument('-gfileout', dest = 'gfileout', type = str, required=True,  help = 'genobaypass outfile')
parser.add_argument('-snpdetout', dest = 'snpdetout', type = str, required=True,  help = 'snpdet outfile')
parser.add_argument('-maf', dest = 'maf', type = float, required=True,  help = 'minimum MAF')



args = parser.parse_args()

out_geno = open(args.gfileout, 'w')
out_snpdet = open(args.snpdetout, 'w')

for line_gfile, line_snpdet in izip(open(args.gfile), open(args.snpdet)):
	dat = line_gfile.split(' ')
	ref_g1 = map(int, [ dat[i] for i in range(0,args.g1*2,2)])
	alt_g1 = map(int, [ dat[i] for i in range(1,args.g1*2,2)])
	ref_g2 = map(int,[ dat[i] for i in range((args.g1*2),(args.g1+args.g2)*2,2)])
	alt_g2 = map(int,[ dat[i] for i in range((args.g1*2)+1,(args.g1+args.g2)*2,2)])
	g1_AF = sum(ref_g1) / (sum(ref_g1)+sum(alt_g1))
	g2_AF = sum(ref_g2) / (sum(ref_g2)+sum(alt_g2))
	if g1_AF >= args.maf and g1_AF <= (1-args.maf) and g2_AF >= args.maf and g2_AF <= (1-args.maf):
		out_geno.write(line_gfile)
		out_snpdet.write(line_snpdet)
		print(line_snpdet)
	else:
		pass
			