from __future__ import division
import sys
import numpy as np
from StringIO import StringIO
import argparse
import math
import os

## Code adapted from Siewert et al. 2018 to calculate NCD statistic from Bitarello et al. 2018
def find_win_indx(prevStarti, prevEndi, SNPi, dataList, winSize):
	locSNP = dataList[SNPi,0] #the coordinates of the core SNP
	winStart = locSNP-winSize/2
	firstI= prevStarti + np.searchsorted(dataList[prevStarti:,0],winStart,side='left') #array index of start of window, inclusive
	winEnd = locSNP + winSize/2
	endI = prevEndi - 1 + np.searchsorted(dataList[prevEndi:,0],winEnd,side='right') #array index of end of window, exclusive
	return(firstI,endI)


def calc_NCD(SNPFreqList, tf):
	NCDnum = 0
	for i in range(len(SNPFreqList)):
		freq = float(SNPFreqList[i,0]) / int(SNPFreqList[i,1])
		if freq > 0.5:
			freq = 1-freq
		NCDnum += (freq-tf)**2
	NCD = math.sqrt(NCDnum / len(SNPFreqList))

	return NCD


def main():
	
	#Loads the input parameters given by the user
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="Name of input file with all SNPs",type=str,required=True)
	parser.add_argument("-o", help="Output file",type=str,default="/dev/stdout")
	parser.add_argument("-w", help="Maximum Window Size (in bp) to calculate NCD in for a single test SNP",type=int,default=1000)
	parser.add_argument("-m", help="Minimum folded core SNP frequency, exclusive",type=float,default=0)


	args = parser.parse_args()


	output = open(args.o,'w')


	#Check for valid file format and parameters
	try:
		SNPs = np.loadtxt(open(args.i,'r'),dtype=float)
	except IOError:
		print sys.exit("Error: Input file cannot be found")
	except:
		print sys.exit("Error: Input file in wrong format")
	if args.m<0 or args.m>.5:
		print sys.exit("Error: Parameter m must be between 0 and 0.5.")
	if len(SNPs.shape)<=1:
		print sys.exit("Error: There must be at least two SNPs in the input file.")


	prevStarti = 0
	prevEndi = 0
	for SNPi in range(len(SNPs)):
		loc = int(SNPs[SNPi,0])
		freqCount = float(SNPs[SNPi,1])
		sampleN = int(SNPs[SNPi,2])
		freq = freqCount/sampleN

		if freq<1.0-args.m and freq>args.m:
			core_loc = SNPs[SNPi,0]
			SNPLocs = SNPs[:,0]
			sI,endI = find_win_indx(prevStarti, prevEndi, SNPi, SNPs, args.w)
			prevStarti = sI
			prevEndi = endI
			if endI>sI:
				SNPSet = np.take(SNPs,range(sI,SNPi+1)+range(SNPi+1,endI+1),axis=0)[:,1:] # adjusted to include core SNP
				NCD_tf5 = calc_NCD(SNPSet,0.5)
				NCD_tf4 = calc_NCD(SNPSet,0.4)
				NCD_tf3 = calc_NCD(SNPSet,0.3)
				output.write(str(loc)+"\t"+str(NCD_tf5)+"\t"+str(NCD_tf4)+"\t"+str(NCD_tf3)+"\n")

		elif freq>1.0 or freq<0:
			print sys.exit("Error: Input file contains SNP of invalid frequency on line "+str(SNPi)+".")




if __name__ == "__main__":
    main()
