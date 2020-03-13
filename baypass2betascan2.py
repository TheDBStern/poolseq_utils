#!/usr/bin/env python
from __future__ import division
import glob, os
import sys
import argparse
import numpy
import random

parser = argparse.ArgumentParser(description='Script to convert a file from multipopulation BayPass format (Scaffold position refcount1 altcount1 etc.) to BetaScan format. Infers ancestral allele count and includes fixed sites. Splits by chromosome and population. Requires two species where populations are assumed to be grouped by species')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input file')
parser.add_argument('-n1', dest = 'numPops1', type = int, required=True,  help = 'number of populations of species 1')
parser.add_argument('-n2', dest = 'numPops2', type = int, required=True,  help = 'number of populations of species 2')
parser.add_argument('-m', dest = 'maf', type = float, required=True,  help = 'minimum MAF for SNP to be included. Evaluated for each pop separately')

args = parser.parse_args()

numPops = args.numPops1+args.numPops2

for i in range(1,numPops+1):
	if not os.path.isdir('pop'+str(i)):
		os.mkdir('pop'+str(i))

with open(args.input,'rU') as f:
	for line in f:
		pcount = 1
		scaf = line.split(' ')[0]
		pos = line.split(' ')[1]
		sp1_A= []
		sp1_a= []
		sp2_A= []
		sp2_a= []
		for pop in range(0,args.numPops1*2,2): #get counts for sp1
			c1 = int(line.split(' ')[pop+2]) # get first allele count for each pop
			c2 = int(line.split(' ')[pop+3]) # second allele count
			sp1_A.append(c1)
			sp1_a.append(c2)
		for pop in range(args.numPops1*2,numPops*2,2): #get counts for sp2
			c1 = int(line.split(' ')[pop+2]) # get first allele count for each pop
			c2 = int(line.split(' ')[pop+3]) # second allele count
			sp2_A.append(c1)
			sp2_a.append(c2)
			
		for pop in range(0,numPops*2,2):
			output = open('pop'+str(pcount)+'/'+str(scaf), 'a')
			c1 = int(line.split(' ')[pop+2]) # get first allele count
			c2 = int(line.split(' ')[pop+3]) # second allele count
			tot = c1 + c2
			sp1_freq = numpy.sum(sp1_A) / (numpy.sum(sp1_A) + numpy.sum(sp1_a))
			sp2_freq = numpy.sum(sp2_A) / (numpy.sum(sp2_A) + numpy.sum(sp2_a))

			if pop / 2 < (numPops - args.numPops1): # species 1
				if sp1_freq == 0 or sp1_freq == 1: # fixed in species 1	
					if sp2_freq == 0 or sp2_freq == 1: # fixed in species 2 so subsitutution		
						output.write(str(pos)+'\t'+str(tot)+'\t'+str(tot)+'\n')
					else:
						pass
				elif c1 == 0 or c2 == 0: # fix in this pop but not in the clade. I.E. lost mutation, not needed
					pass
				elif float(c1 / tot) < args.maf or float(c1 / tot) > (1-args.maf): # needs to pass maf filter
					pass
				elif sp2_freq == 0: # fixed in species 2, a is ancestral
					output.write(str(pos)+'\t'+str(c1)+'\t'+str(tot)+'\n')
				elif sp2_freq ==1:  # fixed in species 2, A is ancestral
					output.write(str(pos)+'\t'+str(c2)+'\t'+str(tot)+'\n')
				else: # variable in both species so assign ancestral to major allele in species 2
					if sp2_freq >= 0.5:
						output.write(str(pos)+'\t'+str(c2)+'\t'+str(tot)+'\n')
					else:
						output.write(str(pos)+'\t'+str(c1)+'\t'+str(tot)+'\n')
			else: #species 2
				if sp2_freq == 0 or sp2_freq == 1: # fixed in species 2
					if sp1_freq == 0 or sp1_freq == 1: # fixed in species 1 so subsitutution		
						output.write(str(pos)+'\t'+str(tot)+'\t'+str(tot)+'\n')
					else:
						pass
				elif c1 == 0 or c2 == 0: # fix in this pop but not in the clade. I.E. lost mutation, not needed
					pass
				elif float(c1 / tot) < args.maf or float(c1 / tot) > (1-args.maf): # needs to pass maf filter
					pass
				elif sp1_freq == 0: # fixed in species 1, a is ancestral
					output.write(str(pos)+'\t'+str(c1)+'\t'+str(tot)+'\n')
				elif sp1_freq ==1:  # fixed in species 1, A is ancestral
					output.write(str(pos)+'\t'+str(c2)+'\t'+str(tot)+'\n')
				else: # variable in both species so assign ancestral to major allele in species 2
					if sp1_freq >= 0.5:
						output.write(str(pos)+'\t'+str(c2)+'\t'+str(tot)+'\n')
					else:
						output.write(str(pos)+'\t'+str(c1)+'\t'+str(tot)+'\n')
			pcount +=1