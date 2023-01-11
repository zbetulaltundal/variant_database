
# database utils
import io
import psycopg2 as psql
import numpy as np
import pandas as pd
import os
import allel
import time
from sqlalchemy import create_engine

from data_configs import *
import config
from main import app
from utils import err_handler
from df_utils import (
    check_df,
    join_data_frames
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



def fetch_from_psql_db_df(conn, query, col_mapper, drop_cols=None):

    try:
        df = pd.read_sql_query(query, con=conn)
        if drop_cols is not None:
            df.drop(columns=drop_cols, inplace=True)
        df.rename(columns = col_mapper, inplace = True)
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
        civic_q = f"""select * from info where id in
                (select info_id from variant where {where});"""
        
        engine = create_engine(f"{config.DB_STRING}/{config.CIVIC_DB_NAME}")
        info_df = pd.read_sql_query(civic_q, con=engine)

        if check_df(info_df) == False:
            drop_cols = ["ID"]
            if 'VT' in info_df: drop_cols.append("CIViC_Variant_Name")
            if 'GN' in info_df: drop_cols.append("SYMBOL")

            info_df.drop(columns=drop_cols, inplace=True)
            info_df.rename(columns = civic_col_name_mapper, inplace = True)
        
        civic_q2 = f"select * from variant where {where});"
        variant_df = pd.read_sql_query(civic_q2, con=engine)
        if check_df(variant_df): 
            variant_df.drop(columns=["ID", "INFO_ID", "FILTER"], inplace=True)
            variant_df.rename(columns={"VAR_ID":"dbSNP RefSNP ID"})
        
        df_merged = join_data_frames(info_df, variant_df)
        return df_merged
    except Exception as err:
        err_handler(err)
        return None


def fetch_from_clingen(hgnc_gene_symbol):
    
    conn = db_connect('clingen') 
    where = f""" WHERE GENE_SYMBOL='{hgnc_gene_symbol}' """
    return fetch_from_psql_db_df(conn, 
            f"""SELECT * FROM clingen_variants {where}""", 
            clingen_col_name_mapper)
        
def fetch_from_pharmgkb(hgnc_gene_symbol):
    try:
        conn = db_connect('pharmgkb') 
        where = f""" WHERE GENE='{hgnc_gene_symbol}' """
        pharmgkb_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM pharmgkb {where}""", pharmgkb_col_name_mapper)
        # drugs_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM drug {where}""", pharmgkb_col_name_mapper)
        # phenotype_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM phenotype {where}""", pharmgkb_col_name_mapper)

        #merged = join_data_frames(data_frames, "", join_type)
        return pharmgkb_df
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

def fetch_from_clinvar(where):
    try:
        info_q = f"""select * from info where id in
                (select info_id from variant where {where});"""

        engine = create_engine(f"{config.DB_STRING}/{config.CLINVAR_DB_NAME}")

        info_df = pd.read_sql_query(info_q, con=engine)
        if check_df(info_df) == False:
            drop_cols = ["ID"]
            info_df.drop(columns=drop_cols, inplace=True)
            info_df.rename(columns = clinvar_info_col_name_mapper, inplace = True)
        
        var_q = f"select * from variant where {where});"
        variant_df = pd.read_sql_query(var_q, con=engine)
        if check_df(variant_df): 
            variant_df.drop(columns=["ID", "FILTER", "INFO_ID"], inplace=True)
            variant_df.rename(columns={"CLINVAR_ID":"ClinVar Variation ID"})
        
        df_merged = join_data_frames(info_df, variant_df)

        return df_merged
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
            civic_df = fetch_from_civic(where)
            clinvar_df = fetch_from_clinvar(where)
            clingen_df = None
            pharmgkb_df = None
            uniprot_df = None

            data_frames = [civic_df, clinvar_df]
            df_joined = join_data_frames(data_frames, ["CHROM","POS","REF","ALT" "HGNC GENE SYMBOL"])
            
            if check_df(df_joined):
                hgnc_symbol = df_joined.loc[0]["HGNC GENE SYMBOL"]
                clingen_df = fetch_from_clingen(hgnc_symbol)
                pharmgkb_df = fetch_from_pharmgkb(hgnc_symbol)
                #uniprot_df = fetch_from_uniprot(hgnc_symbol)
                data_frames = [clingen_df, pharmgkb_df, uniprot_df]
                df_joined = join_data_frames(data_frames, ["HGNC GENE SYMBOL"])


            out_arr.append(df_joined)

        return out_arr
    
    except Exception as err:
        err_handler(err)
        return None
