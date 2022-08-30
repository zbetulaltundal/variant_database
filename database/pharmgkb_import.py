import os
import vcf
import main

def import_PharmGKB(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    vcf_path = f'{cwd}\\data\\CIVic'
    vcf_name = 'nightly-civic_accepted_and_submitted.vcf'
    vcf_reader = vcf.Reader(open(f'{vcf_path}\\{vcf_name}'))

    # open .tsv file
    with open("GeekforGeeks.tsv") as f:
   
        # Read data line by line
        for line in f:
            
            # split data by tab
            # store it in list
            l=line.split('\t')
            
            # append list to ans
            print(l)
