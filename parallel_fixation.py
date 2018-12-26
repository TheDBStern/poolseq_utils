#!/usr/bin/env python

from __future__ import division
import glob, os
import sys
import argparse
import numpy
from itertools import izip


parser = argparse.ArgumentParser(description='Script to find SNPs that are fixed in some subset of populations, but not the others')
parser.add_argument('-gfile', dest = 'gfile', type = str, required=True,  help = 'input genobaypass file')
parser.add_argument('-snpdet', dest = 'snpdet', type = str, required=True,  help = 'input snpdet file')
parser.add_argument('-sel', dest = 'sel', nargs='+',type = int, required=True,  help = 'list of population with shared selective pressure of interest')
parser.add_argument('-non', dest = 'non', nargs='+',type = int, required=True,  help = 'list of population without the shared selective pressure of interest')
parser.add_argument('-o', dest = 'outfile', type = str, required=True,  help = 'genobaypass outfile')
parser.add_argument('-maf', dest = 'maf', type = float, required=True,  help = 'minimum MAF for groups to be considered polymorphic or fixed')


args = parser.parse_args()

outfile = open(args.outfile, 'w')

def is_polymorphic(candidate):
    for n in range(2, candidate):
        if candidate % n == 0:
            return False
    return True

for line_gfile, line_snpdet in izip(open(args.gfile), open(args.snpdet)):
	dat = line_gfile.split(' ')
	snpdet = line_snpdet.split(' ')
	ref_sel_pos = [ (i*2)-2 for i in args.sel]
	alt_sel_pos = [ (i*2)-1 for i in args.sel]
	ref_non_pos = [ (i*2)-2 for i in args.non]
	alt_non_pos = [ (i*2)-1 for i in args.non]
	ref_sel = map(int, [ dat[i] for i in ref_sel_pos ] )
	alt_sel = map(int, [ dat[i] for i in alt_sel_pos ] )
	ref_non = map(int, [ dat[i] for i in ref_non_pos ] )
	alt_non = map(int, [ dat[i] for i in alt_non_pos ] )
	sel_AF = sum(ref_sel) / (sum(ref_sel)+sum(alt_sel))
	#non_AF = sum(ref_non) / (sum(ref_non)+sum(alt_non))
	non_AF = [ (x / (x+y)) for x,y in izip(ref_non,alt_non) ]
	if sel_AF <= args.maf or sel_AF >= (1-args.maf):
		if all( i >= args.maf and i <= (1-args.maf) for i in non_AF):
		#if non_AF >= args.maf and non_AF <= (1-args.maf):
			info = ' '.join(snpdet[0:2])
			outfile.write(info+' Sel: '+str(sel_AF)+' Non: '+str(non_AF)+'\n')
	else:
		pass
			