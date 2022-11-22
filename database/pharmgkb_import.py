from functools import reduce
import math
import os
import sys
import common_functions
import pandas as pd

join_cols = ['Clinical Annotation ID']

dataset_to_db_col_mapper = {'Clinical Annotation ID': 'Clinical_Annotation_ID', 'Variant/Haplotypes': 'VARIANT', 'Gene': 'GENE', 'Level of Evidence': 'LEVEL_OF_EVIDENCE', 'Level Override': 'LEVEL_OVERRIDE', 'Level Modifiers': 'LEVEL_MODIFIERS', 'Score_x': 'SCORE', 'Phenotype Category': 'PHENOTYPE_CATEGORY', 'PMID Count': 'PMID_COUNT', 'Evidence Count': 'EVIDENCE_COUNT', 'Latest History Date (YYYY-MM-DD)': 'LATEST_HISTORY_DATE', 'URL': 'pharmgkb_URL', 'Specialty Population': 'Specialty_Population', 'Genotype/Allele': 'Genotype', 'Annotation Text': 'ANNOTATION_TEXT', 'Allele Function': 'Allele_Function', 'Evidence ID': 'Evidence_ID', 'Evidence Type': 
'Evidence_Type', 'Evidence URL': 'Evidence_URL', 'PMID': 'Evidence_PMID', 'Summary': 'Evidence_Summary', 'Score_y': 'Evidence_Score'}

def tsv_to_df(folder_path, filename):
    try:
        full_path = folder_path + filename
        tsv_file = pd.read_csv(full_path, sep = '\t')

        return tsv_file
    except Exception as err:
        common_functions.err_handler(err)

def join_data_frames(data_frames):

    try:
        df_merged = reduce(lambda  left,right: pd.merge(left,right, on=join_cols, how='inner'), data_frames)
        return df_merged

    except Exception as err:
        common_functions.err_handler(err)

def split_drugs_and_phenotypes(str_val):

    l_str_val = str_val.split(";")[:-1]
    if(len(l_str_val) == 0): return f"('{str_val}')"

    res_str = ""
    for elem in l_str_val:
        res_str = f"{res_str},('{elem}')"

    return res_str[1:]


def insert_drug_data(drug_list_str, conn):
    try:
        if common_functions.check_value(drug_list_str): 
            drug_records = split_drugs_and_phenotypes(drug_list_str)
            query = f"""INSERT INTO DRUG (DRUG) VALUES {drug_records} RETURNING id;"""
            return str(common_functions.insert_into_db_returning_id_v2(conn, query))
        else: return None
        
    except Exception as err:
        common_functions.err_handler(err)
        return None


def insert_phenotype_data(phenotype_list_str, conn):
    try:
        if common_functions.check_value(phenotype_list_str):
            p_records = split_drugs_and_phenotypes(phenotype_list_str)
            query = f"""INSERT INTO PHENOTYPE (PHENOTYPE_NAME) VALUES {p_records} RETURNING id;"""
            p_id = str(common_functions.insert_into_db_returning_id_v2(conn, query))
            return p_id
        else: return None
        
    except Exception as err:
        common_functions.err_handler(err)
        return None

def set_to_not_scored(score_y):
    try:
        if common_functions.check_value(score_y):
            if score_y == 'This annotation is not used for clinical annotation scoring.':
                return 'NS'
            else: return score_y
        else: return None
    except Exception as err:
        common_functions.err_handler(err)

def insert_csv(conn):
    
    try:
        cwd = os.getcwd()
        fpath = f'{cwd}\\temp\\pharmgkb_tbl.csv'
        cur = conn.cursor()
        query = f'''COPY pharmgkb
            FROM '{fpath}'
            DELIMITER ','
            CSV HEADER; '''

        cur.execute(query)
        conn.commit()
    except Exception as err:
        print ("Exception has occured:", err)
        print ("Exception type:", type(err))
        err_type, err_obj, traceback = sys.exc_info()
        line_num = traceback.tb_lineno
        # print the connect() error
        print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print ("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)

        # print the pgcode and pgerror exceptions
        print ("pgerror:", err.pgerror)
        print ("pgcode:", err.pgcode, "\n")
        conn.rollback()

            
def insert_df(conn, df):
    
    try:
        #add 'drug_id' column to end of DataFrame and insert drug values to database
        df['DRUG_ID'] = df['Drug(s)'].apply(lambda x: insert_drug_data(x, conn))

        #add 'phenotype_id' column to end of DataFrame and insert phenotype values to database
        df['PHENOTYPE_ID'] = df['Phenotype(s)'].apply(lambda x: insert_phenotype_data(x, conn))

        # rename not scored records as 'NS'
        if 'Score_y' in df.columns:
            df['Score_y'] = df['Score_y'].apply(set_to_not_scored)
        
        # drop unnecessary columns
        df.drop(columns=['Drug(s)', 'Phenotype(s)'], inplace=True)

        df.rename(columns = dataset_to_db_col_mapper, inplace = True)

        df.to_csv("temp\\pharmgkb_tbl.csv")

        insert_csv(conn)

    except Exception as err:
        common_functions.err_handler(err)

def import_pharmgkb(conn):
    
    try:
        # open the csv
        cwd = os.getcwd()  # Get the current working directory
        folder_path = f'{cwd}\\data\\clinicalAnnotations\\'
        filenames = ["clinical_annotations.tsv", "clinical_ann_alleles.tsv", "clinical_ann_evidence.tsv"]
        data_frames = []
        for filename in filenames:
            df = tsv_to_df(folder_path, filename)
            data_frames.append(df)
        
        df_merged = join_data_frames(data_frames)

        insert_df(conn, df_merged)

    except Exception as err:
        common_functions.err_handler(err)
