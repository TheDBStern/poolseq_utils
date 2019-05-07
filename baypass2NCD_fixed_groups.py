#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy
from itertools import izip


parser = argparse.ArgumentParser(description='Script to find fixed differences between 2 groups of populations and create a NCD-style output file')
parser.add_argument('-gfile', dest = 'gfile', type = str, required=True,  help = 'input genobaypass file')
parser.add_argument('-snpdet', dest = 'snpdet', type = str, required=True,  help = 'input snpdet file')
parser.add_argument('-g1', dest = 'g1', type = int, required=True,  help = 'number of pops in group 1 (assuming from the start)')
parser.add_argument('-g2', dest = 'g2', type = int, required=True,  help = 'number of pops in group 2 (assuming the last ones)')
parser.add_argument('-ncdout_g1', dest = 'ncdout_g1', type = str, required=True,  help = 'fixed differences file for group 1')
parser.add_argument('-ncdout_g2', dest = 'ncdout_g2', type = str, required=True,  help = 'fixed differences file for group 2')



args = parser.parse_args()

ncdout_g1 = open(args.ncdout_g1, 'w')
ncdout_g2 = open(args.ncdout_g2, 'w')


for line_gfile, line_snpdet in izip(open(args.gfile), open(args.snpdet)):
	dat = line_gfile.split(' ')
	snpinfo = line_snpdet.split(' ')
	ref_allele = snpinfo[3]
	alt_allele = snpinfo[4]
	ref_g1 = map(int, [ dat[i] for i in range(0,args.g1*2,2)])
	alt_g1 = map(int, [ dat[i] for i in range(1,args.g1*2,2)])
	ref_g2 = map(int,[ dat[i] for i in range((args.g1*2),(args.g1+args.g2)*2,2)])
	alt_g2 = map(int,[ dat[i] for i in range((args.g1*2)+1,(args.g1+args.g2)*2,2)])
	g1_AF = sum(ref_g1) / (sum(ref_g1)+sum(alt_g1))
	g2_AF = sum(ref_g2) / (sum(ref_g2)+sum(alt_g2))
	if g2_AF == 0 or g2_AF == 1:
		ncdout.write(
	else:
		pass
			