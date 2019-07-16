#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to split a sync or genotype file by scaffold if the first item in the line in the scaffold name')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-d', dest = 'delim', type = str, required=True,  help = 'field delimiter')
parser.add_argument('-k', dest = 'keep', action ='store_true', default= False, help ='retain the scaffold name in the line')
args = parser.parse_args()


with open(args.input,'rU') as f:
	for line in f:
		scaf = line.split(args.delim)[0]
		output = open(args.input.split('/')[-1]+'_'+scaf, 'a')
		if args.keep:
			output.write(line)
		else:
			output.write(' '.join(line.split(args.delim)[1:]))