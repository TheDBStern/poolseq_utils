#!/usr/bin/env python

import argparse
import numpy as np
import time
import progressbar

parser = argparse.ArgumentParser(description='Script to calculate the top X percentage of coverage across all pools')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input sync file')
parser.add_argument('-q', dest = 'quantile', type = float, required=True,  help = 'coverage percentile to calculate (e.g. 0.99 will calculate coverage at top 99%% of sites')

args = parser.parse_args()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
print("Calculating file length")
flen = file_len(args.input)
print("Done")
cov_dat = []
pbar = progressbar.ProgressBar(maxval=int(flen))
pbar.start()

with open(args.input,'rU') as f:
	i=1
	for line in f:
		popdat = line.split('\t')[3:]
		for pop in popdat:
			cov = sum(map(int,pop.split(':')))
			cov_dat.append(cov)
		time.sleep(0.05)
		pbar.update(i+1)
		i +=1
pbar.finish()

cov_dat = np.array(cov_dat)
top_cov = int(np.quantile(cov_dat, args.quantile,interpolation="nearest"))
print("Result: 'max-coverage %s' is equivalent to 'max-coverage %s'\n"%(args.quantile,top_cov))
