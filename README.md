# poolseq_utils
Scripts to manipulate allele frequency files used in PoolSeq analyses, specifically for 'Balancing selection in the native range promotes parallel adaptation during invasions.' All scripts have some description and help info accessible with -h or --help.

* NCD1_snpwise.py Calculates NCD1 scores (Bitarello et al. 2018) on a per-snp (rather than genomic window) basis, similar to BetaScan (Siewert & Voight 2017)
* baypass2bayescan.py Creates BayeScan formatted input files from the 'genobaypass' output file generated in poolfstat
Currently, baypass2bayescan.py needs to be followed up with \
`cat header.txt tmp* > outfile` \
`rm header.txt tmp* `
* baypass2betascan.py Script to convert a file from multipopulation BayPass format (Scaffold position refcount1 altcount1 etc.) to BetaScan format with fixed sites removed. Splits by chromosome and population.
* baypass2betascan2.py Script to convert a file from multipopulation BayPass format (Scaffold position refcount1 altcount1 etc.) to BetaScan format including substitutions and polarizing SNP frequencies. Requires two sets of populations with one used as the outgroup for the other.
* bed_to_gene_list.py Script to get blast result names from bedfile with gene names
* filter_baypass_groupwise_MAF.py Script to filter snps that have a MAF below some threshold in one group (right now works for two groups)
* snps_to_regions.soft_around.py This script takes a list of significant SNP locations and converts it to a bed file of regions of interest. One can specify the window size and number of significant SNPs requires to be in the window. Overlapping windows are combined.
