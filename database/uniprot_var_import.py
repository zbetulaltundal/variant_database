import pandas as pd
from tqdm import tqdm
import timeit
from os import getcwd

# custom functions

from utils import(
    err_handler,
    check_value,
    write_csv
)

from db_utils import(
    insert_csv
)

cols=['Gene Name', 'AC', 'Variant AA Change', 'Source DB ID', 'Consequence Type', 'Clinical Significance', 'Phenotype/Disease', 'Phenotype/Disease Source', 'Cytogenetic Band', 'Chromosome Coordinate', 'Ensembl gene ID', 'Ensembl transcript ID', 'Ensembl translation ID', 'Evidence']
db_cols = ['gene_name', 'AC', 'variant_aa_change', 'source_db_id', 'consequence_type', 'clinical_significance', 'phenotype_disease', 'phenotype_disease_source', 'cytogenetic_band', 'chromosome_coordinate', 'ensembl_gene_ID', 'ensembl_transcript_ID', 'ensembl_translation_ID']

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
    # skip first 327 rows since they just give information about data
    main_df = pd.read_csv(file_name, 
            skiprows=327,  
            sep='\t', 
            names=cols, 
            dtype=str,
            header=0,
            chunksize=1000000)

    # 38.200.897 records 
    t_1 = timeit.default_timer()
    elapsed_time = round((t_1 - t_0) * 10 ** 9, 3)
    print(f"uniprot data is read in {elapsed_time} ms")
    #df = pd.concat(chunks)

    t_0 = timeit.default_timer()

    cwd = getcwd()
    for df in tqdm(main_df):
        for col in cols:
            df[col] = df[col].apply(replace_dash)

        df = df.drop(columns=["Evidence"])
        df.rename(columns=db_dict, inplace=True)
        write_csv(df, f"{cwd}\\temp\\uniprot_variant.csv")
        variant_cols = "gene_name,AC,variant_aa_change,source_db_id,consequence_type,clinical_significance,phenotype_disease,phenotype_disease_source,cytogenetic_band,chromosome_coordinate,ensembl_gene_ID,ensembl_transcript_ID,ensembl_translation_ID"
        insert_csv(conn, f"{cwd}\\temp\\uniprot_variant.csv", "variant", variant_cols)

        df['id'] = df['variant_aa_change'].apply(lambda x: get_id(x, conn))
        # chunk of evidence data
        ev_df = pd.concat([df['evidence_name'].str.split(','), df['id']], axis=1, keys=['evidence_name', 'variant_id']).reset_index()
        ev_df = ev_df.explode('evidence_name')
        write_csv(ev_df, f"{cwd}\\temp\\uniprot_evidence.csv")
        insert_csv(conn, f"{cwd}\\temp\\uniprot_evidence.csv", "evidence", "evidence_name, variant_id")