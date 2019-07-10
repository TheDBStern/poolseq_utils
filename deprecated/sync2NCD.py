#!/usr/bin/env python
from __future__ import division

import glob, os
import sys
import argparse
import numpy
import random

parser = argparse.ArgumentParser(description='Script to generate NCD-style files from a sync file with two groups of populations')
parser.add_argument('-i', dest = 'input', type = str, required=True,  help = 'input sync file')
parser.add_argument('-m', dest = 'mincov', type = int, required=True,  help = 'minimum coverage to be met by all populations')
parser.add_argument('-M', dest = 'maxcov', type = int, required=True,  help = 'maximum coverage to be met by all populations')
parser.add_argument('-g1', dest = 'group1', type = int, nargs='+', required=True,  help = 'indices of populations in group1/ species1 (starting with 1)')
parser.add_argument('-g2', dest = 'group2', type = int, nargs='+', required=True,  help = 'indices of populations in group2/ species2 (starting with 1)')
parser.add_argument('-maf', dest = 'maf', type = float, required=True,  help = 'minimum minor allele frequency to consider fixed')


args = parser.parse_args()

sync_dict = {0:'A',1:'T',2:'C',3:'G'}


pops = args.group1 + args.group2
for pop in pops:
	if not os.path.isdir("./pop"+str(pop)):
		os.mkdir("./pop"+str(pop))
pop_pos = []
for x in pops:
	i = x+2
	pop_pos.append(i)

def get_min_coverage(line):
	covs = []
	popdat = line.split('\t')
	for i in pop_pos:
		pop = popdat[i]
		cov = sum(map(int,pop.split(':')[0:4]))
		covs.append(cov)
	return(min(covs))

def get_max_coverage(line):
	covs = []
	popdat = line.split('\t')
	for i in pop_pos:
		pop = popdat[i]
		cov = sum(map(int,pop.split(':')[0:4]))
		covs.append(cov)	
	return(max(covs))


def is_fixed(line):
	dat = line.split('\t')
	g1_a_count = 0
	g1_t_count = 0
	g1_c_count = 0
	g1_g_count = 0

	g2_a_count = 0
	g2_t_count = 0
	g2_c_count = 0
	g2_g_count = 0
	for pop in args.group1:
		counts = dat[pop+2]
		a_count = int(counts.split(':')[0])
		g1_a_count = g1_a_count+ a_count
		t_count = int(counts.split(':')[1])
		g1_t_count = g1_t_count+ t_count
		c_count = int(counts.split(':')[2])
		g1_c_count = g1_c_count+ c_count
		g_count = int(counts.split(':')[3])
		g1_g_count = g1_g_count+ g_count
	for pop in args.group2:
		counts = dat[pop+2]
		a_count = int(counts.split(':')[0])
		g2_a_count = g2_a_count+ a_count
		t_count = int(counts.split(':')[1])
		g2_t_count = g2_t_count+ t_count
		c_count = int(counts.split(':')[2])
		g2_c_count = g2_c_count+ c_count
		g_count = int(counts.split(':')[3])
		g2_g_count = g2_g_count+ g_count
		
	g1_total = g1_a_count + g1_t_count + g1_c_count +g1_g_count
	g2_total = g2_a_count + g2_t_count + g2_c_count +g2_g_count
	g1_AFs = [g1_a_count/g1_total,g1_t_count/g1_total,g1_c_count/g1_total,g1_g_count/g1_total]
	g2_AFs = [g2_a_count/g2_total,g2_t_count/g2_total,g2_c_count/g2_total,g2_g_count/g2_total]
	
	if any(x > (1-args.maf) for x in g1_AFs) and any(x > (1-args.maf) for x in g2_AFs):
		g1_fixed = numpy.where(numpy.array(g1_AFs) > (1-args.maf))
		g2_fixed = numpy.where(numpy.array(g2_AFs) > (1-args.maf))
		if g1_fixed != g2_fixed:
			return True
		else:
			return False

def get_ref_alt_allele(line,pops):
	dat = line.split('\t')
	#ref = dat[2]

	allele_counts = [0,0,0,0]
	for pop in pops:
		counts = map(int,dat[pop+2].split(':'))
		for i in range(0,4):
			allele_counts[i] =+ counts[i]
	
	tot = sum(allele_counts)
	AFs = []
	for i in allele_counts:
		AFs.append(i/tot)
	
	AFs = numpy.array(AFs)
	ref = sync_dict[numpy.where(AFs == max(AFs))[0][0]]
	if numpy.sort(AFs)[2] != 0:
		alt = numpy.where(AFs == numpy.sort(AFs)[2])[0]
		if len(alt) > 1:
			alt1 = sync_dict[alt[0]]
			alt2 = sync_dict[alt[1]]
			alt = [alt1,alt2]
		elif len(alt) == 1:
			alt = sync_dict[alt[0]]
		if numpy.sort(AFs)[1] != 0 and len(alt) == 1:
			alt2 = numpy.where(AFs == numpy.sort(AFs)[1])[0]
			alt2 = sync_dict[alt2[0]]
			alt = [alt,alt2]
	elif numpy.sort(AFs)[2] == 0:
		alt = random.choice(['A','C','T','G'])
		while (alt == ref):
			alt = random.choice(['A','C','T','G'])
	return([ref,alt])
	
	
with open(args.input,'rU') as f:
	for line in f:
		dat = line.split('\t')
		mincov = get_min_coverage(line)
		maxcov = get_max_coverage(line)	
		scaf = line.split('\t')[0]
		pos = line.split('\t')[1]
		scafnum = scaf.strip('Scaffold')
		ID = scafnum+'|'+pos
		if mincov < args.mincov or maxcov > args.maxcov:
			pass
		else:
			### NCD SNP Format: CHR POS ID REF ALT AF1 AF2 AF3 MAF
			### NCD Format: CHR	POS	REF	Chimp_REF	ID
			g1_ref_alt = get_ref_alt_allele(line,args.group1)
			g2_ref_alt = get_ref_alt_allele(line,args.group2)
			for pop in pops:
				output = open('pop'+str(pop)+'/'+str(scaf), 'a')
				output_FD = open('pop'+str(pop)+'/'+str(scaf)+'_FD', 'a')				
				counts = map(int,dat[pop+2].split(':')[0:4])
				tot = sum(counts)
				AFs = []
				for i in counts:
					AFs.append(i/tot)
				AFs.sort()
				AF1 = round(AFs[3],4)
				AF2 = round(AFs[2],4)
				if AF1 >  (1-args.maf):
					AF1 = 1
					AF2 = 0
					AF3 = 'NA'
					MAF = 0
				elif AF1 < (1-args.maf) and AFs[1]==0:
					MAF = AF2
					AF3 = 'NA'
				else:
					AF3 = round(AFs[1],4)
					MAF = AF3
				if pop in args.group1:
					output.write(scafnum+'\t'+pos+'\t'+ID+'\t'+g1_ref_alt[0]+'\t'+','.join(g1_ref_alt[1])+'\t'+str(AF1)+'\t'+str(AF2)+'\t'+str(AF3)+'\t'+str(MAF)+'\n')
					if is_fixed(line):
						output_FD.write(scafnum+'\t'+pos+'\t'+g1_ref_alt[0]+'\t'+','.join(g2_ref_alt[0])+'\t'+ID+'\n')
				elif pop in args.group2:
					output.write(scafnum+'\t'+pos+'\t'+ID+'\t'+g2_ref_alt[0]+'\t'+','.join(g2_ref_alt[1])+'\t'+str(AF1)+'\t'+str(AF2)+'\t'+str(AF3)+'\t'+str(MAF)+'\n')
					if is_fixed(line):
						output_FD.write(scafnum+'\t'+pos+'\t'+g2_ref_alt[0]+'\t'+','.join(g1_ref_alt[0])+'\t'+ID+'\n')
				