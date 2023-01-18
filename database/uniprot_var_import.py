import pandas as pd
from tqdm import tqdm
import timeit
from os import getcwd
from sqlalchemy import create_engine

# custom functions

from utils import(
    err_handler,
    check_value,
    write_csv
)

from db_utils import(
    insert_csv,
    fetch_one
)

from db_config import(
    DB_STRING,
    UNIPROTVAR_DB_NAME
)

cols=['Gene Name', 'AC', 'Variant AA Change', 'Source DB ID', 'Consequence Type', 'Clinical Significance', 'Phenotype/Disease', 'Phenotype/Disease Source', 'Cytogenetic Band', 'Chromosome Coordinate', 'Ensembl gene ID', 'Ensembl transcript ID', 'Ensembl translation ID', 'Evidence']
db_cols = ['gene_name', 'AC', 'variant_aa_change', 'source_db_id', 'consequence_type', 'clinical_significance', 'phenotype_disease', 'phenotype_disease_source', 'cytogenetic_band', 'chromosome_coordinate', 'ensembl_gene_ID', 'ensembl_transcript_ID', 'ensembl_translation_ID']
special_cols=['Gene Name', 'AC', 'Variant AA Change']
db_dict = {'Gene Name': 'gene_name', 'AC': 'AC', 
'Variant AA Change': 'variant_aa_change', 
'Source DB ID': 'source_db_id', 
'Consequence Type': 'consequence_type', 
'Clinical Significance': 'clinical_significance', 
'Phenotype/Disease': 'phenotype_disease', 
'Phenotype/Disease Source': 'phenotype_disease_source', 
'Cytogenetic Band': 'cytogenetic_band', 
'Chromosome Coordinate': 'chromosome_coordinate', 
'Ensembl gene ID': 'ensembl_gene_ID', 
'Ensembl transcript ID': 'ensembl_transcript_ID', 'Ensembl translation ID': 'ensembl_translation_ID', 'Evidence':'evidence_name'}

file_name = "data\\homo_sapiens_variation.txt\\homo_sapiens_variation.txt"


def get_id(variant_aa_change, conn):
    try:
        cur = conn.cursor()
        query = f"""select id from variant where 
            variant_aa_change='{variant_aa_change}'"""
        cur.execute(query)
        res = cur.fetchall()
        id = res[0][0]
        return id
    except Exception as err:
        err_handler(err)
        return None

def replace_dash(x):
    try:
        if check_value(x) and x != '-': return x
        return None
    except Exception as err:
        err_handler(err)
        return None

def import_uniprot(conn):
    
    t_0 = timeit.default_timer()
    chunksize = 1000000
    # skip first 327 rows since they just give information about data
    main_df = pd.read_csv(file_name, 
            skiprows=327,  
            sep='\t', 
            names=cols, 
            dtype=str,
            header=0,
            chunksize=chunksize)

    
    engine = create_engine(f"{DB_STRING}/{UNIPROTVAR_DB_NAME}")
    # 38.200.897 records 
    t_1 = timeit.default_timer()
    elapsed_time = round((t_1 - t_0) * 10 ** 9, 3)
    print(f"uniprot data is read in {elapsed_time} ms")
    #df = pd.concat(chunks)

    t_0 = timeit.default_timer()
    try:
        cwd = getcwd()
        ctr = 0
        initial_count = fetch_one(conn, "select count(*) from variant;")
        initial_count = initial_count[0]
        for df in tqdm(main_df):
            for col in special_cols:
                df[col] = df[col].apply(replace_dash)

            df.rename(columns=db_dict, inplace=True)
            df_t = df.drop(columns=["evidence_name"])
            write_csv(df_t, f"{cwd}\\temp\\uniprot_variant.csv", index=False)
            variant_cols = "gene_name,AC,variant_aa_change,source_db_id,consequence_type,clinical_significance,phenotype_disease,phenotype_disease_source,cytogenetic_band,chromosome_coordinate,ensembl_gene_ID,ensembl_transcript_ID,ensembl_translation_ID"
            insert_csv(conn, f"{cwd}\\temp\\uniprot_variant.csv", "variant", variant_cols)

            offset = chunksize*ctr + initial_count
            res_df = pd.read_sql_query(f'select id from variant offset{offset} limit {chunksize}', con=engine)
            df['id'] = res_df['id']
            # insert chunk of evidence data
            ev_df = pd.concat([df['evidence_name'].str.split(','), df['id']], axis=1, keys=['evidence_name', 'variant_id']).reset_index()
            ev_df = ev_df.explode('evidence_name')
            ev_df.drop(columns=["index"], inplace=True)
            write_csv(ev_df, f"{cwd}\\temp\\uniprot_evidence.csv", index=False)
            insert_csv(conn, f"{cwd}\\temp\\uniprot_evidence.csv", "evidence", "evidence_name, variant_id")
            ctr = ctr + 1
    except Exception as err:
        err_handler(err)
        return None
