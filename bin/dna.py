#!/usr/bin/env python

# no __future__ division!
import string, sys, math

############################################################
# fasta
#
# Common methods for dealing with fasta files
############################################################

############################################################
# fasta2dict
#
# Read a multifasta file into a dict.  Taking the whole line
# as the key.
############################################################
def fasta2dict(fasta_file):
    fasta_dict = {}
    
    header = ''
    seq = ''
    
    for line in open(fasta_file):
        if line[0] == '>':
            #header = line.split()[0][1:]
            header = line[1:].rstrip()
            fasta_dict[header] = ''
        else:
            fasta_dict[header] += line.rstrip()

    return fasta_dict


############################################################
# rc
#
# Reverse complement sequence
############################################################
def rc(seq):
    return seq.translate(string.maketrans("ATCGatcg","TAGCtagc"))[::-1]


############################################################
# count_kmers
#
# Count kmers from forward and reverse strand
############################################################
def count_kmers(k, seq, all=False):
    kmers = {}
    N = len(seq)
    rc_seq = rc(seq)
    for i in range(N-k+1):
        # forward
        kmer = seq[i:i+k]
        if kmers.has_key(kmer):
            kmers[kmer] += 1
        else:
            kmers[kmer] = 1

        # reverse
        kmer = rc_seq[i:i+k]
        kmer = seq[i:i+k]
        if kmers.has_key(kmer):
            kmers[kmer] += 1
        else:
            kmers[kmer] = 1

    # remove non-ACGT kmers
    nts = {'A':1, 'C':1, 'G':1, 'T':1}
    for kmer in kmers.keys():
        for nt in kmer:
            if not nts.has_key(nt):
                del kmers[kmer]
                break

    if all:
        # add zero count kmers        
        for i in range(int(math.pow(4,k))):
            kmer = int2kmer(k,i)
            if not kmers.has_key(kmer):
                kmers[kmer] = 0                
                
    return kmers

############################################################
# int2kmer
#
# Map integers to kmers
############################################################
def int2kmer(k,num):
    nts = ['A','C','G','T']
    kmer = ''
    for x in range(k):
        b = int(math.pow(4, k-1-x))
        kmer += nts[num / b]
        num =  num % b
    return kmer


############################################################
# canonical_kmers
#
# Clean up a dict of kmer counts by combining kmers with
# their reverse complements.  All counts are then divided
# by 2.  Careful about palindromes.
############################################################
def canonical_kmers(kmers, return_all=False):
    canon_kmers = {}
    for kmer in kmers:
        kmer_rc = rc(kmer)
            
        if kmer < kmer_rc:
            # add current
            if canon_kmers.has_key(kmer):
                canon_kmers[kmer] += kmers[kmer] / 2.0
            else:
                canon_kmers[kmer] = kmers[kmer] / 2.0

        elif kmer_rc < kmer:
            # add current
            if canon_kmers.has_key(kmer_rc):
                canon_kmers[kmer_rc] += kmers[kmer] / 2.0
            else:
                canon_kmers[kmer_rc] = kmers[kmer] / 2.0

        elif kmer == kmer_rc:
            # add once, divide by 2 bc we double counted it
            #  once on each strand
            canon_kmers[kmer] = kmers[kmer] / 2.0

    if return_all:
        # add back reverse complements
        for kmer in kmers:
            if not canon_kmers.has_key(kmer):
                canon_kmers[kmer] = canon_kmers[rc(kmer)]

    return canon_kmers


############################################################
# nt_composition
#
# Return a dict of the nt counts in the given sequence,
# making no assumptions about what the sequence components
# are.
############################################################
def nt_composition(seq):
    comp = {}
    for nt in seq:
        if comp.has_key(nt):
            comp[nt] += 1
        else:
            comp[nt] = 1
    return comp


############################################################
# nt_composition_file
#
# Return a dict of the nt counts of the sequences in the
# given file making no assumptions about what the sequence
# components are.
############################################################
def nt_composition_file(seq_file):
    comp = {}
    for line in open(seq_file):
        if line[0] != '>':
            for nt in line.rstrip():
                if comp.has_key(nt):
                    comp[nt] += 1
                else:
                    comp[nt] = 1
    return comp

############################################################
# translate
#
# Translate a dna sequence into an amino acid.  Attempts
# to maintain lowercase or uppercase.  If a codon contains
# both lowercase and uppercase, returns a lowercase codon.
############################################################
code = {     'TTT': 'F', 'TCT': 'S', 'TAT': 'Y', 'TGT': 'C', \
             'TTC': 'F', 'TCC': 'S', 'TAC': 'Y', 'TGC': 'C', \
             'TTA': 'L', 'TCA': 'S', 'TAA': '*', 'TGA': '*', \
             'TTG': 'L', 'TCG': 'S', 'TAG': '*', 'TGG': 'W', \
             'CTT': 'L', 'CCT': 'P', 'CAT': 'H', 'CGT': 'R', \
             'CTC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R', \
             'CTA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R', \
             'CTG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R', \
             'ATT': 'I', 'ACT': 'T', 'AAT': 'N', 'AGT': 'S', \
             'ATC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S', \
             'ATA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R', \
             'ATG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R', \
             'GTT': 'V', 'GCT': 'A', 'GAT': 'D', 'GGT': 'G', \
             'GTC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G', \
             'GTA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G', \
             'GTG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G', \

             'ttt': 'f', 'tct': 's', 'tat': 'y', 'tgt': 'c', \
             'ttc': 'f', 'tcc': 's', 'tac': 'y', 'tgc': 'c', \
             'tta': 'l', 'tca': 's', 'taa': '*', 'tga': '*', \
             'ttg': 'l', 'tcg': 's', 'tag': '*', 'tgg': 'w', \
             'ctt': 'l', 'cct': 'p', 'cat': 'h', 'cgt': 'r', \
             'ctc': 'l', 'ccc': 'p', 'cac': 'h', 'cgc': 'r', \
             'cta': 'l', 'cca': 'p', 'caa': 'q', 'cga': 'r', \
             'ctg': 'l', 'ccg': 'p', 'cag': 'q', 'cgg': 'r', \
             'att': 'i', 'act': 't', 'aat': 'n', 'agt': 's', \
             'atc': 'i', 'acc': 't', 'aac': 'n', 'agc': 's', \
             'ata': 'i', 'aca': 't', 'aaa': 'k', 'aga': 'r', \
             'atg': 'm', 'acg': 't', 'aag': 'k', 'agg': 'r', \
             'gtt': 'v', 'gct': 'a', 'gat': 'd', 'ggt': 'g', \
             'gtc': 'v', 'gcc': 'a', 'gac': 'd', 'ggc': 'g', \
             'gta': 'v', 'gca': 'a', 'gaa': 'e', 'gga': 'g', \
             'gtg': 'v', 'gcg': 'a', 'gag': 'e', 'ggg': 'g' \
             }

def translate(dna):
    if len(dna) % 3 != 0:
        print 'DNA sequence is not have length divisible by 3.'
        return ''
    else:
        i = 0
        peptide = ''
        while i < len(dna):
            if code.has_key(dna[i:i+3]):
                peptide += code[dna[i:i+3]]
            else:
                peptide += code[dna[i:i+3].lower()]
            i += 3
        return peptide

############################################################
# __main__
############################################################
if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--comp':
        nt_comp = nt_composition_file(sys.argv[2])
        sum = sum(nt_comp.values())
        for nt in nt_comp:
            print '%s %d (%f)' % (nt,nt_comp[nt],nt_comp[nt]/sum)
    elif len(sys.argv) == 3 and sys.argv[1] == '--rc':
        print rc(sys.argv[2])
    else:
        print 'Usage: ./fasta.py --comp <seq_file>'