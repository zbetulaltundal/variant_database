from functools import reduce
import math
import os
import main
import pandas as pd

join_cols = ['Clinical Annotation ID']

def tsv_to_df(folder_path, filename):
    try:
        full_path = folder_path + filename
        tsv_file = pd.read_csv(full_path, sep = '\t')

        return tsv_file
    except Exception as err:
        main.err_handler(err)

def join_data_frames(data_frames):

    try:
        df_merged = reduce(lambda  left,right: pd.merge(left,right, on=join_cols, how='outer'), data_frames)
        return df_merged

    except Exception as err:
        main.err_handler(err)

def insert_df(conn, df):
    
    try:
        for index, row in df.iterrows():

            drugs = row['Drug(s)']
            if main.check_var(drugs) != None: 
                drug_list = drugs.split(';')
                nDrugs = len(drug_list)
                format_spec = (nDrugs-1) * ',%s'
                query = f"""INSERT INTO DRUG (DRUG) VALUES (%s {format_spec}) RETURNING id;"""
                record = tuple(drug_list)
                drug_id = main.insert_into_db_returning_id(conn, query, record)
            else: drug_id = None

            phenotypes = row['Phenotype(s)']
            if main.check_var(phenotypes) != None: 
                query = "INSERT INTO PHENOTYPE (PHENOTYPE_NAME) VALUES (%s) RETURNING id;"
                record = (phenotypes)
                phenotype_id = main.insert_into_db_returning_id(conn, query, record)
            else: phenotype_id = None

            if math.isnan(row['PMID']) == True:
                row['PMID'] = 0

            # insert record into the PHARMGKB table
            query = """INSERT INTO PHARMGKB (Clinical_Annotation_ID, VARIANT, GENE, \
                            LEVEL_OF_EVIDENCE, LEVEL_OVERRIDE, LEVEL_MODIFIERS, SCORE, PHENOTYPE_CATEGORY, \
                            PMID_COUNT, EVIDENCE_COUNT, LATEST_HISTORY_DATE, pharmgkb_URL, \
                            Specialty_Population, Genotype, ANNOTATION_TEXT, Allele_Function, \
                            Evidence_ID, Evidence_Type, Evidence_URL, Evidence_PMID, Evidence_Summary, \
                            Evidence_Score, DRUG_ID, PHENOTYPE_ID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                %s, %s, %s, %s, %s, %s);"""

            if 'Score_y' in row and row['Score_y'] == 'This annotation is not used for clinical annotation scoring.':
                    row['Score_y'] = 'NS'

            row.drop(labels=['Drug(s)', 'Phenotype(s)'], inplace=True)
            foreign_keys = pd.Series([drug_id, phenotype_id])
            f_row = pd.concat([row, foreign_keys], ignore_index=True)
            record = (tuple(f_row))
            main.insert_into_db(conn, query, record)


    except Exception as err:
        main.err_handler(err)

def import_pharmgkb(conn):
    
    try:
        # open the csv data
        cwd = os.getcwd()  # Get the current working directory
        folder_path = f'{cwd}\\data\\pharmgkb\\clinicalAnnotations\\'
        filenames = ["clinical_annotations.tsv", "clinical_ann_alleles.tsv", "clinical_ann_evidence.tsv"]
        data_frames = []
        for filename in filenames:
            df = tsv_to_df(folder_path, filename)
            data_frames.append(df)
        
        df_merged = join_data_frames(data_frames)
        #f_df = df_merged.where(pd.notnull(df_merged), None)
        
        insert_df(conn, df_merged)

    except Exception as err:
        main.err_handler(err)

