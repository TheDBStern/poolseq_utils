#!/usr/bin/env python

import argparse
import numpy as np
import time
import progressbar
from joblib import Parallel, delayed
import multiprocessing

parser = argparse.ArgumentParser(description='Script to calculate the top X percentage of coverage across all pools')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input sync file')
parser.add_argument('-q', dest = 'quantile', type = float, required=True,  help = 'coverage percentile to calculate (e.g. 0.99 will calculate coverage at top 99%% of sites')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'output file')


args = parser.parse_args()

output = open(args.output, 'w')
    
def calc_cov_per_line(line):
	popdat = line.split('\t')[3:]
	for pop in popdat:
		cov = sum(map(int,pop.split(':')))
	return(cov)

print("Calculating maximum coverage cutoffs from the empirical distributions of coverages")
num_cores = multiprocessing.cpu_count()
cov_dat = []

with open(args.input,'rU') as f:
	cov = Parallel(n_jobs=num_cores)(delayed(calc_cov_per_line)(line) for line in f)
	cov_dat.append(cov)

cov_dat = np.array(cov_dat)
top_cov = int(np.quantile(cov_dat, args.quantile,interpolation="nearest"))
print("Done")
output.write("Result: 'max-coverage %s' is equivalent to 'max-coverage %s'\n"%(args.quantile,top_cov))
