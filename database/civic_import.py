import os 
import re
import sys
import io
import pandas as pd

from config import (
    CIVIC_DATA_PATH
)

from db_utils import(
    insert_csv,
    insert_into_db_returning_id_V1,
)

from utils import(
    check_var,
    read_vcf,
    err_handler
)

civic_csq_cols=['Allele', 'Consequence', 'SYMBOL', 'Entrez Gene ID',
 'Feature_type', 'Feature', 'HGVSc', 'HGVSp', 'CIViC Variant Name', 
 'CIViC Variant ID', 'CIViC Variant Aliases', 'CIViC HGVS', 
 'Allele Registry ID', 'ClinVar IDs', 'CIViC Variant Evidence Score', 'CIViC Entity Type', 'CIViC Entity ID', 
 'CIViC Entity URL', 'CIViC Entity Source', 'CIViC Entity Variant Origin', 'CIViC Entity Status', 'CIViC Entity Clinical Significance', 'CIViC Entity Direction', 'CIViC Entity Disease', 'CIViC Entity Drugs', 'CIViC Entity Drug Interaction Type', 'CIViC Evidence Phenotypes', 'CIViC Evidence Level', 'CIViC Evidence Rating', 'CIViC Assertion ACMG Codes', 'CIViC Assertion AMP Category', 'CIViC Assertion NCCN Guideline', 'CIVIC Assertion Regulatory Approval', 'CIVIC Assertion FDA Companion Test']

def replace_cols(l):
    l_new = []
    for item in l:
        l_new.append(item.replace(" ", "_"))
    return l_new

csq_pattern = re.compile("##INFO\s*=<\s*ID\s*=\s*CSQ*", flags=re.IGNORECASE)
def get_csq_fields(path):
    
    fields = []
    with open(path, 'r') as f:
        for line in f:
            if csq_pattern.match(line) is not None:
                start_idx = line.find("Format: ") + 8
                fields = line[start_idx: ].split("|")
                return fields

    return fields

def insert_info_to_db(info_str, conn):
    
    try:
        info_list = info_str.split(";")

        info_dict = dict(
            GN="",
            VT=""
            )
        

        for info_pair in info_list:
            item_data = info_pair.split("=")
            key = item_data[0]
            val = item_data[1]

            if key=="CSQ":
                for csq_val, csq_key in zip(val.split("|"), civic_csq_cols):
                    t_csq_val = check_var(csq_val)
                    csq_key_f = csq_key.replace(" ", "_")
                    info_dict[csq_key_f] = t_csq_val

            if key in info_dict:
                info_dict[key] = val
                if key=="GN": print(info_dict[key])

        info_id = None
        
        info_values = info_dict.values()

        # 89th line gives an exception
        # if len(info_values) == 33: 
        #     print(info_values)
        query = f"""INSERT INTO  INFO (GN, VT, Allele,Consequence,SYMBOL,Entrez_Gene_ID, \
        Feature_type,Feature,HGVSc,HGVSp,CIViC_Variant_Name,CIViC_Variant_ID,CIViC_Variant_Aliases,\
        CIViC_HGVS,Allele_Registry_ID,ClinVar_IDs,CIViC_Variant_Evidence_Score,\
        CIViC_Entity_Type,CIViC_Entity_ID,CIViC_Entity_URL,CIViC_Entity_Source,\
        CIViC_Entity_Variant_Origin,CIViC_Entity_Status,CIViC_Entity_Clinical_Significance,\
        CIViC_Entity_Direction,CIViC_Entity_Disease,CIViC_Entity_Drugs,CIViC_Entity_Drug_Interaction_Type,\
        CIViC_Evidence_Phenotypes,CIViC_Evidence_Level,CIViC_Evidence_Rating,CIViC_Assertion_ACMG_Codes,CIViC_Assertion_AMP_Category,CIViC_Assertion_NCCN_Guideline,CIVIC_Assertion_Regulatory_Approval,CIVIC_Assertion_FDA_Companion_Test)
        VALUES"""
        format_spec =f' ({(len(info_values) -1)*("%s,")} %s) RETURNING ID;'
        record=tuple(info_values)
        info_id = insert_into_db_returning_id_V1(conn, f"{query}{format_spec}", record)

        return info_id

    except Exception as err:
        print("in function insert_info_to_db")
        err_handler(err)

def print_list(l):
    for item in l:
        print(f"{item}", end =",")

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})


def import_civic_data(conn):
    
    cwd = os.getcwd()  # Get the current working directory
    vcf_path = f'{cwd}\\{CIVIC_DATA_PATH}' 
    df = read_vcf(vcf_path)

    df['INFO_ID'] = df['INFO'].progress_apply(insert_info_to_db, conn=conn)
    df.drop(columns="INFO", inplace=True)
    df.to_csv("temp\\civic_variants.csv", index=False)
    cwd = os.getcwd()
    fpath = f'{cwd}\\temp\\civic_variants.csv'
    insert_csv(conn, fpath, "VARIANT", "CHROM,POS,VAR_ID,REF,ALT,QUAL,FILTER,INFO_ID")
