
from os import getcwd
import pandas as pd
from sqlalchemy import create_engine

from utils import(
    err_handler,
    check_value,
    join_data_frames,
    tsv_to_df,
    write_csv
)

from db_utils import(
    insert_into_db_returning_id_V2,
    insert_csv
)

from db_config import (
    PHARMGKB_DB_NAME,
    DB_STRING
)

join_cols = ['Clinical Annotation ID']

dataset_to_db_col_mapper = {'Clinical Annotation ID': 'Clinical_Annotation_ID', 'Variant/Haplotypes': 'VARIANT', 'Gene': 'GENE', 'Level of Evidence': 'LEVEL_OF_EVIDENCE', 'Level Override': 'LEVEL_OVERRIDE', 'Level Modifiers': 'LEVEL_MODIFIERS', 'Score_x': 'SCORE', 'Phenotype Category': 'PHENOTYPE_CATEGORY', 'PMID Count': 'PMID_COUNT', 'Evidence Count': 'EVIDENCE_COUNT', 'Latest History Date (YYYY-MM-DD)': 'LATEST_HISTORY_DATE', 'URL': 'pharmgkb_URL', 'Specialty Population': 'Specialty_Population', 'Genotype/Allele': 'Genotype', 'Annotation Text': 'ANNOTATION_TEXT', 'Allele Function': 'Allele_Function', 'Evidence ID': 'Evidence_ID', 'Evidence Type': 
'Evidence_Type', 'Evidence URL': 'Evidence_URL', 'PMID': 'Evidence_PMID', 'Summary': 'Evidence_Summary', 'Score_y': 'Evidence_Score'}

def split_drugs_and_phenotypes(str_val):
    l_str_val = str_val.split(";")[:-1]
    if(len(l_str_val) == 0): return str_val

    res_str = ""
    for elem in l_str_val:
        res_str += ", " + elem

    return res_str[1:]


def get_drug_data(drug_list_str):
    try:
        if check_value(drug_list_str): 
            drug_records = split_drugs_and_phenotypes(drug_list_str)
            return drug_records
        else: return None
        
    except Exception as err:
        err_handler(err)
        return None


def get_phen_data(phenotype_list_str):
    try:
        if check_value(phenotype_list_str):
            p_records = split_drugs_and_phenotypes(phenotype_list_str)
            return p_records
        else: return None
        
    except Exception as err:
        err_handler(err)
        return None

def set_to_not_scored(score_y):
    try:
        if check_value(score_y):
            if score_y == 'This annotation is not used for clinical annotation scoring.':
                return 'NS'
            else: return score_y
        else: return None
    except Exception as err:
        err_handler(err)
   
def insert_df(conn, df):
    
    try:
        cwd = getcwd()
        df.rename(columns = dataset_to_db_col_mapper, inplace = True)

        # rename not scored records as 'NS'
        if 'Score_y' in df.columns:
            df['Score_y'] = df['Score_y'].apply(set_to_not_scored)
        
        var_df = df.drop(columns=['Drug(s)', 'Phenotype(s)', 'VARIANT'])
        
        write_csv(var_df, f"{cwd}\\temp\\pharmgkb_variant.csv", index=False)
       
        insert_csv(conn, f"{cwd}\\temp\\pharmgkb_variant.csv", "variant", """Clinical_Annotation_ID, GENE, LEVEL_OF_EVIDENCE, LEVEL_OVERRIDE,
             LEVEL_MODIFIERS, SCORE, PHENOTYPE_CATEGORY, PMID_COUNT, EVIDENCE_COUNT,
             LATEST_HISTORY_DATE, pharmgkb_URL, Specialty_Population, Genotype,
             ANNOTATION_TEXT, Allele_Function, Evidence_ID, Evidence_Type, Evidence_URL, 
             Evidence_PMID, Evidence_Summary, Evidence_Score""")
        
        engine = create_engine(f"{DB_STRING}/{PHARMGKB_DB_NAME}")
        res_df = pd.read_sql_query(f'select id from variant', con=engine)
        df['id'] = res_df['id']

        df['Drug(s)'] = df['Drug(s)'].apply(get_drug_data)
        drug_df = pd.concat([df['Drug(s)'].str.split(","), df['id']], axis=1, keys=["drug_name", "variant_id"]).reset_index()
        drug_df = drug_df.explode('drug_name')
        drug_df.drop(columns=["index"], inplace=True)
        write_csv(drug_df, f"{cwd}\\temp\\pharmgkb_drugs.csv", index=False)
        insert_csv(conn, f"{cwd}\\temp\\pharmgkb_drugs.csv", "DRUG", "drug_name, variant_id")

        df['Phenotype(s)'] = df['Phenotype(s)'].apply(get_phen_data)
        phen_df = pd.concat([df['Phenotype(s)'].str.split(","), df['id']], axis=1, keys=["phenotype_name", "variant_id"]).reset_index()
        phen_df = phen_df.explode('phenotype_name')
        phen_df.drop(columns=["index"], inplace=True)
        write_csv(phen_df, f"{cwd}\\temp\\pharmgkb_phenotypes.csv", index=False)
        insert_csv(conn, f"{cwd}\\temp\\pharmgkb_phenotypes.csv", "PHENOTYPE", "phenotype_name, variant_id")

        variant_df = pd.concat([df['VARIANT'].str.split(","), df['id']], axis=1, keys=["variant_name", "variant_id"]).reset_index()
        variant_df = variant_df.explode('variant_name')
        variant_df.drop(columns=["index"], inplace=True)
        write_csv(variant_df, f"{cwd}\\temp\\pharmgkb_haplotypes.csv", index=False)
        insert_csv(conn, f"{cwd}\\temp\\pharmgkb_haplotypes.csv", "HAPLOTYPE", "variant_name, variant_id")

    except Exception as err:
        err_handler(err)

def import_pharmgkb(conn):
    
    try:
        # open the csv
        cwd = getcwd()  # Get the current working directory
        folder_path = f'{cwd}\\data\\clinicalAnnotations\\'
        filenames = ["clinical_annotations.tsv", "clinical_ann_alleles.tsv", "clinical_ann_evidence.tsv"]
        data_frames = []
        for filename in filenames:
            df = tsv_to_df(folder_path, filename)
            data_frames.append(df)
        
        df_merged = join_data_frames(data_frames, join_cols)

        insert_df(conn, df_merged)

    except Exception as err:
        err_handler(err)
