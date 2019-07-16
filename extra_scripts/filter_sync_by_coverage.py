#!/usr/bin/env python

import glob, os
import sys
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to filter a sync file by min and max coverage')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input sync file to filter')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'name of output')
parser.add_argument('-m', dest = 'mincov', type = int, required=True,  help = 'minimum coverage to be met by all populations')
parser.add_argument('-M', dest = 'maxcov', type = int, required=True,  help = 'maximum coverage to be met by all populations')

args = parser.parse_args()

out = open(args.output,'w')

with open(args.input,'rU') as f:
	for line in f:
		popdat = line.split('\t')[3:]
		covs = []
		for pop in popdat:
			cov = sum(map(int,pop.split(':')))
			covs.append(cov)
		if any(x < args.mincov for x in covs) or any(x > args.maxcov for x in covs):
			pass
		else:
			out.write(line)
			