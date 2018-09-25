#!/usr/bin/env python

import glob, os
import argparse
import numpy

parser = argparse.ArgumentParser(description='Script to convert a file from BayPass format to BayeScan format')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input baypass format file')
parser.add_argument('-o', dest = 'output', type = str, required=True,  help = 'name of output')
parser.add_argument('-p', dest = 'pops', type = int, required=True,  help = 'number of pools')

args = parser.parse_args()

## func to determine length of file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
flen = file_len(args.input)

#generate header lines
head = open('header.txt','w')
head.write('[loci]=%s\n\n[populations]=%s\n\n'%(str(flen),str(args.pops)))

#create tmp file for each pop
for i in range(1,args.pops+1):
	output = open('tmp'+str(i),'w')
	output.write('[pop]=%s\n'%(i))

with open(args.input,'rU') as f:
	lcount = 1
	for line in f:
		pcount = 1
		for pop in range(0,args.pops*2,2):
			c1 = int(line.split(' ')[pop]) # get first allele count for each pop
			c2 = int(line.split(' ')[pop+1]) # second allele count
			tot = c1 + c2
			output = open('tmp'+str(pcount),'a')
			#output.write('%s %s 2 %s %s\n'%(lcount,tot,c1,c2))
			output.write('{:>6} {:>3} 2 {:>3} {:>3}\n'.format(lcount,tot,c1,c2))
			pcount +=1
		lcount +=1

#fnames = sorted(glob.glob('tmp*'))
#fnames.insert(0,'header.txt')
#print(fnames)
#with open(args.output, 'w') as outfile:
#    for fname in fnames:
#        with open(fname) as infile:
#            for line in infile:
#                outfile.write(line)
		
#for file in glob.glob('tmp*'):
#	os.remove(file)
#os.remove('header.txt')