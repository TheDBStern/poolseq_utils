#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

'''
Would be nice to split for all populations
'''

parser = argparse.ArgumentParser(description='Script to convert a file from an altered BayPass format (position freq total) to BetaScan format with variants removed if at 0 or 100%')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'name of output')

args = parser.parse_args()

output = open(args.output, 'w')
with open(args.input,'rU') as f:
	for line in f:
		tot = int(line.split(' ')[1]) + int(line.split(' ')[2])
		if int(line.split(' ')[1]) == 0 or int(line.split(' ')[2]) == 0:
			pass
		else:
			output.write(line.split(' ')[0]+' '+line.split(' ')[1]+' '+str(tot)+'\n')