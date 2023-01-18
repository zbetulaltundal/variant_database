# database utilities

import psycopg2 as psql
import pandas as pd
import os
import functools 
from sqlalchemy import create_engine

import config
from main import app

from utils import (
    err_handler,
    check_df,
    join_data_frames
)
from data_configs import (
    clingen_col_name_mapper,
    civic_col_name_mapper,
    clinvar_mapper,
    uniprot_col_mapper,
    pharmgkb_mapper
)

def db_connect(db_name):
    try:
        conn = psql.connect(
            host=config.HOST_NAME,
            port=config.PORT_NAME,
            database=db_name,
            user=config.DB_USER,
            password=config.DB_PWD
            )

        print("Database connected successfully")
        return conn
    except Exception as err:
        err_handler(err)



def fetch_from_psql_db_df(engine, query, col_mapper=None, drop_cols=None):

    try:
        df = pd.read_sql_query(query, con=engine)
        if drop_cols is not None:
            df.drop(columns=drop_cols, inplace=True)
        
        if col_mapper is not None: df.rename(columns=col_mapper, inplace = True)
        return df
    
    except Exception as err:
        err_handler(err)
        return None


def get_info(info_id, info_df_list, conn):
    try:
        civic_q = f"""SELECT * FROM info WHERE ID={info_id}"""   
        info_df = pd.read_sql_query(civic_q, con=conn)
        info_df_list.append(info_df)
        return info_df
    except Exception as err:
        err_handler(err)
        return None


def fetch_from_civic(where):
    try:
        civic_q = f"""select * from variant
            INNER JOIN INFO on VARIANT.INFO_ID = INFO.ID {where};"""
        
        engine = create_engine(f"{config.DB_STRING}/{config.CIVIC_DB_NAME}")
        df = pd.read_sql_query(civic_q, con=engine)

        if check_df(df):
            drop_cols = ["id", "info_id", "filter"]
            if "gn" in df: drop_cols.append("Symbol")
            if "vt" in df: drop_cols.append("CIViC Variant Name")
            df.rename(columns = civic_col_name_mapper, inplace = True)
            df.drop(columns=drop_cols, inplace=True)

        return df
    except Exception as err:
        err_handler(err)
        return None


def fetch_from_clingen(hgnc_gene_symbol):
    
    engine = create_engine(f"{config.DB_STRING}/{config.CLINGEN_DB_NAME}")

    where = f""" WHERE GENE_SYMBOL='{hgnc_gene_symbol}' """
    df = fetch_from_psql_db_df(engine, 
            f"""SELECT * FROM clingen_variants {where}""", 
            clingen_col_name_mapper)
    if check_df(df):
        df.drop(columns=['id'], inplace=True)
        
    return df 


def fetch_from_pharmgkb(hgnc_gene_symbol):
    try:    
        engine = create_engine(f"{config.DB_STRING}/{config.PHARMGKB_DB_NAME}")
        where = f""" WHERE GENE='{hgnc_gene_symbol}' """

        pharmgkb_df = fetch_from_psql_db_df(engine,f"""SELECT * FROM variant {where}""", pharmgkb_mapper)
        drugs_df = fetch_from_psql_db_df(engine,f"""SELECT * FROM drug where VARIANT_ID in (select id from variant {where})""", {"drug_name":"pharmgkb drug names"})
        phenotype_df = fetch_from_psql_db_df(engine,f"""SELECT * FROM phenotype  where VARIANT_ID in (select id from variant {where})""", {"phenotype_name":"pharmgkb phenotypes"})
        haplotype_df = fetch_from_psql_db_df(engine,f"""SELECT * FROM haplotype  where VARIANT_ID in (select id from variant {where})""", {"variant_name":"pharmgkb haplotypes"})
        
        if check_df(drugs_df): 
            drugs_df.dropna(inplace=True)
            drugs_df = (drugs_df.groupby(['variant_id']).agg({'pharmgkb drug names': lambda x: None if x is None else",".join(x)}).reset_index())
        if check_df(phenotype_df): 
            phenotype_df.dropna(inplace=True)
            phenotype_df = (phenotype_df.groupby(['variant_id']).agg({'pharmgkb phenotypes': lambda x: None if x is None else",".join(x)}).reset_index())
        if check_df(haplotype_df): 
            haplotype_df.dropna(inplace=True)
            haplotype_df = (haplotype_df.groupby(['variant_id']).agg({'pharmgkb haplotypes': lambda x: None if x is None else",".join(x)}).reset_index())
        
        merged = join_data_frames([pharmgkb_df, drugs_df, phenotype_df, haplotype_df], ["variant_id"], "inner")

        if check_df(merged): 
            merged.drop(columns=["variant_id"], inplace=True)
            merged.rename(columns=pharmgkb_mapper,inplace=True)
        return merged
    except Exception as err:
        err_handler(err)
        return None

def fetch_from_uniprot(hgnc_gene_symbol):
    
    try:
        where = f"where gene_name = '{hgnc_gene_symbol}'"
        engine = create_engine(f"{config.DB_STRING}/{config.UNIPROT_DB_NAME}")
        df = fetch_from_psql_db_df(engine,f"SELECT * FROM variant {where}", uniprot_col_mapper)
        evidence_df = fetch_from_psql_db_df(engine,f"SELECT variant_id,evidence_name FROM evidence  where VARIANT_ID in (select id from variant {where})")
        
        if check_df(evidence_df): 
            evidence_df.dropna(inplace=True)
            evidence_df = (evidence_df.groupby(['variant_id']).agg({'Uniprot Evidence Names': lambda x: None if x is None else",".join(x)}).reset_index())

        merged = join_data_frames([df, evidence_df], ["variant_id"], "inner")
        if check_df(merged): 
            merged.drop(columns=["variant_id"], inplace=True)
        return merged
    except Exception as err:
        err_handler(err)
        return None

def fetch_one(conn, query):
    try:
        cur = conn.cursor() 
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        conn.commit()
        return res
    except Exception as err:
        err_handler(err)
        return None

# clinvar query generator
def cv_q_gen(cols, tbl_name, where):
    return f"""SELECT {cols}
            FROM {tbl_name} where INFO_ID in
            (select info_id from variant \
            INNER JOIN INFO on VARIANT.INFO_ID = INFO.ID {where})"""


def fetch_from_clinvar(where):
    try:
        q = f"""select CHROM, POS, CLINVAR_ID, REF,ALT, QUAL, INFO_ID, ALLELEID,CLNHGVS,CLNVC,CLNVCSO,ORIGIN,AF_ESP,AF_EXAC,AF_TGP,DBVARID,RS,SSR
            from variant
            INNER JOIN INFO on VARIANT.INFO_ID = INFO.ID {where};"""
        
        engine = create_engine(f"{config.DB_STRING}/{config.CLINVAR_DB_NAME}")
        df = pd.read_sql_query(q, con=engine)
        df.rename(columns=clinvar_mapper, inplace=True)
        if check_df(df)==False: return None
        
        clndisdb_df =  fetch_from_psql_db_df(engine,cv_q_gen("info_id,clndisdb_name, clndisdb_abbrv, clndisdb_id", "clndisdb", where))
        if check_df(clndisdb_df): 

            clndisdb_df["clndisdb"] = clndisdb_df['clndisdb_name'].astype(str) +"("+ clndisdb_df['clndisdb_abbrv'] + ") : "+ clndisdb_df['clndisdb_id']
            clndisdb_df = (clndisdb_df.groupby(['info_id']).agg({"clndisdb": lambda x:None if x is None else", ".join(x)}).reset_index())

        GENEINFO_df =  fetch_from_psql_db_df(engine,cv_q_gen("info_id, gene_symbol, gene_id", "geneinfo", where), {"gene_symbol": "HGNC Gene Symbol"})
        if  check_df(GENEINFO_df): 
            GENESYMBOL_df = (GENEINFO_df.groupby(['info_id']).agg({"HGNC Gene Symbol": lambda x: None if x is None else", ".join(x)}).reset_index())
            GENEINFO_df["Gene Info"] = GENEINFO_df['HGNC Gene Symbol'].astype(str) +":"+ GENEINFO_df['gene_id']
            GENEINFO_df = (GENEINFO_df.groupby(['info_id']).agg({"Gene Info": lambda x: None if x is None else", ".join(x)}).reset_index())

        CLNVI_df =  fetch_from_psql_db_df(engine,cv_q_gen("info_id, src, src_id","CLNVI", where))
        if check_df(CLNVI_df): 
            CLNVI_df["CLNVI"] = CLNVI_df['src'].astype(str) +":"+ CLNVI_df['src_id']
            CLNVI_df = (CLNVI_df.groupby(['info_id']).agg({'CLNVI': lambda x: None if x is None else",".join(x)}).reset_index())

        MC_df =  fetch_from_psql_db_df(engine,cv_q_gen("info_id, sequence_ontology_id, molecular_consequence","MC",where))
        if check_df(MC_df): 
            MC_df["MC"] = MC_df['sequence_ontology_id'].astype(str) +"|"+ MC_df['molecular_consequence']
            MC_df = (MC_df.groupby(['info_id']).agg({'MC': lambda x:None if x is None else ",".join(x)}).reset_index())

        # clnrevstat_df =  fetch_from_psql_db_df(engine,cv_q_gen("info_id, REVIEW_STATUS, NUM_OF_SUBMITTERS, CONFLICT","clnrevstat",where))
        # if check_df(clnrevstat_df): 
        #     clnrevstat_df["Review Status"] = clnrevstat_df['review_status'].astype(str) +"-"+ clnrevstat_df['num_of_submitters'] + "-" +  clnrevstat_df['conflict']
        #     clnrevstat_df = (clnrevstat_df.groupby(['info_id']).agg({'REVIEW STATUS': lambda x:None if x is None else ",".join(x)}).reset_index())

        data_frames = [df, clndisdb_df, GENESYMBOL_df, GENEINFO_df, CLNVI_df, MC_df]

        for val in ["clnsig", "clnsigconf", "clnsigincl"]:
            sub_df =  fetch_from_psql_db_df(engine,cv_q_gen(f"{val}, info_id", val,where))
            if check_df(sub_df): 
                sub_df = (sub_df.groupby(['info_id']).agg({val: lambda x: None if x is None else",".join(x)}).reset_index())
            data_frames.append(sub_df)

        for val in ["clndn", "clndnincl"]:
            sub_df =  fetch_from_psql_db_df(engine,cv_q_gen(f"{val}_gene_symbol, {val}_gene_id, info_id", val,where))
            if check_df(sub_df): 
                sub_df[val] = sub_df[f'{val}_gene_symbol'].astype(str) +":"+ sub_df[f'{val}_gene_id']
                sub_df = (sub_df.groupby(['info_id']).agg({val: lambda x: None if x is None else",".join(x)}).reset_index())
                
            data_frames.append(sub_df)

        
        df_joined = join_data_frames(data_frames, join_cols=["info_id"], join_type="inner")
        if check_df(df_joined):
            drop_cols = list()
            if "info_id" in df: drop_cols.append("info_id")
            if "filter" in df: drop_cols.append("filter")
            df_joined.drop(columns=drop_cols, inplace=True)
           
        return df_joined
    except Exception as err:
        err_handler(err)
        return None

def get_col_name(s):
    try:
        res = []
        l = s.split(";")
        for elem in l:
            key, val = elem.split("=")
            res.append(key)

        return res 
    except Exception as err:
        err_handler(err)
        return None 

def fetch_from_user_db(where):
    try:
        q = f"select * from variant {where}"
        engine = create_engine(f"{config.DB_STRING}/{config.USER_DB_NAME}")
        df = pd.read_sql_query(q, con=engine)
        if check_df(df)==False: return None
        else: 
            info_cols = []
            split_info = df['info'].str.split(';', expand=True)
            for indx, pair in split_info.items():
                key, val = pair[0].split("=")
                info_cols.append(key)
                split_info[indx] = val

            df[info_cols] = split_info
            return df
    except Exception as err:
        err_handler(err)
        return None

def insert_data(df):
    conn = None
    try:
        cwd = os.getcwd()
        fpath=f'{cwd}\\Temp\\inserted.csv'
        df.to_csv(fpath, index=False)
        conn = psql.connect(f"{config.DB_STRING}/{config.USER_DB_NAME}")
        cur = conn.cursor()

        query = f'''COPY VARIANT(CHROM,POS,VAR_ID,REF,ALT,QUAL,FILTER,INFO)
            FROM '{fpath}'
            DELIMITER ','
            CSV HEADER; '''

        cur.execute(query)
        conn.commit()
        conn.close()
        return True
        
    except Exception as err:
        err_handler(err)
        if conn is not None:
            conn.rollback()
            conn.close()

        return False

def append_df(df, data_frames):
    if check_df(df):
        data_frames.append(df)

def list_results(df):
    try:
        out_arr = []

        for index, row in df.iterrows():
            
            CHROM = row['CHROM']
            ALT = row['ALT']
            REF = row['REF']
            POS = row['POS']
            
            where = f""" WHERE ALT='{ALT}' AND\
                    REF='{REF}' AND\
                    POS='{POS}' AND\
                    CHROM='{CHROM}' """
            
            df_joined = None
            
            data_frames = []
            civic_df = fetch_from_civic(where)
            append_df(civic_df, data_frames)
            clinvar_df = fetch_from_clinvar(where)
            append_df(clinvar_df, data_frames)
            #user_df = fetch_from_user_db(where)
            #append_df(user_df, data_frames)

            #df_joined = functools.reduce(lambda left, right: left.join(right, on=["chrom","pos","ref","alt"]), data_frames)
          
            df_joined = join_data_frames(data_frames, ["chrom","pos","ref","alt"])

            if check_df(df_joined):
                if "HGNC Gene Symbol" in df_joined:
                    data_frames = [df_joined]
                    for hgnc_symbol in df_joined["HGNC Gene Symbol"].unique():
                        clingen_df = fetch_from_clingen(hgnc_symbol)
                        append_df(clingen_df, data_frames)
                        pharmgkb_df = fetch_from_pharmgkb(hgnc_symbol)
                        append_df(pharmgkb_df, data_frames)
                        #uniprot_df = fetch_from_uniprot(hgnc_symbol)   
                        #append_df(uniprot_df, data_frames)   

                        #df_joined = functools.reduce(lambda left, right: left.join(right, on="HGNC Gene Symbol"), data_frames)

                        df_joined = join_data_frames([df_joined, pharmgkb_df, clingen_df], ["HGNC Gene Symbol"])

            if check_df(df_joined):
                out_arr.append(df_joined)

        res_df = pd.concat(out_arr)
        return res_df
    
    except Exception as err:
        err_handler(err)
        return None
