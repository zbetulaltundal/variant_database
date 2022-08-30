import os
import vcf
import main
import pandas as pd

def tsv_to_df(folder_path, filename):
    return pd.read_csv(folder_path + filename)

def import_PharmGKB(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    folder_path = f'{cwd}\\data\\PharmGKB\\clinical\\'
    filenames = ["clinical_ann_alleles.tsv", "clinical_ann_evidence.tsv", "clinical_annotations.tsv"]
    data_frames = []
    for filename in filenames:
        df = tsv_to_df(folder_path, filename)
        data_frames.append(df)
        print(df)
    
    