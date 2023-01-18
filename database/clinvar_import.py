# import scikit-allel
from asyncio.windows_events import NULL
from tqdm import tqdm
import sys
import re
import os
import pandas as pd
import timeit

from utils import(
    err_handler,
    check_value
)

from db_utils import(
    insert_csv,
    insert_into_db_returning_id_V1,
    insert_into_db
)

tqdm.pandas()

def insert_into_info_table(conn, info_cols):
    query = """INSERT INTO INFO (AF_ESP, AF_EXAC, AF_TGP, \
                    ALLELEID, CLNHGVS, CLNVC, CLNVCSO, DBVARID, \
                        ORIGIN, RS, SSR)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""

    record = (info_cols["AF_ESP"], info_cols["AF_EXAC"], info_cols["AF_TGP"], info_cols["ALLELEID"], \
    info_cols["CLNHGVS"], info_cols["CLNVC"], info_cols["CLNVCSO"], info_cols["DBVARID"], info_cols["ORIGIN"], info_cols["RS"], info_cols["SSR"])
    
    return insert_into_db_returning_id_V1(conn, query, record)  


def insert_into_clndisdb(conn, disdb_list, info_id):
    record = None
    try:
        query = """INSERT INTO CLNDISDB (CLNDISDB_NAME, CLNDISDB_ABBRV, CLNDISDB_ID, INFO_ID)\
                                                        VALUES (%s, %s, %s, %s);"""
        for elem in disdb_list:
            record = (elem["name"], elem["id"],  elem["abbrv"], info_id)
            insert_into_db(conn, query, record)
    except Exception as err:
        print("in function insert_into_clndisdb")
        print(record, "CLNDİSDB")
        err_handler(err)


def insert_into_clnrevstat(conn, stat_list, info_id):
    try:
        query = f'INSERT INTO CLNREVSTAT (REVIEW_STATUS, NUM_OF_SUBMITTERS, CONFLICT, INFO_ID)\
                    VALUES (%s, %s, %s, %s);'

        for elem in stat_list:
            if type(elem) == list:
                record = (elem, '', '', info_id)
            else: record = (elem["condition"], elem["num_of_submitters"], elem["conflict"], info_id)
            insert_into_db(conn, query, record)
        
    except Exception as err:
        print("CLNDİSDB")
        err_handler(err)
        

def insert_clnsig(conn, clnsig_list, tbl_name, info_id):
    query = f'INSERT INTO {tbl_name} ({tbl_name}, INFO_ID)\
                    VALUES (%s, %s);'

    for elem in clnsig_list:
        record = (elem, info_id)
        insert_into_db(conn, query, record)

def insert_into_MC(conn, mc_list, info_id):
    try:
        query = f'INSERT INTO MC (sequence_ontology_id, molecular_consequence, INFO_ID)\
                        VALUES (%s, %s, %s);'
        
        for elem in mc_list:
            record = (elem["sequence_ontology_id"], elem["molecular_consequence"], info_id)
            insert_into_db(conn, query, record)
    except Exception as err:
        print("in func insert_into_MC")
        err_handler(err)


def insert_into_GENEINFO(conn, gene_list, info_id):
    
    query = "INSERT INTO GENEINFO (GENE_SYMBOL, GENE_ID, INFO_ID) \
        VALUES (%s, %s, %s);"
        
    for elem in gene_list:
        record = (elem['val1'], elem['val2'], info_id)
        insert_into_db(conn, query, record)

def insert_into_CLNVI(conn, clnvi_list, info_id):
    query = "INSERT INTO CLNVI (SRC, SRC_ID, INFO_ID) \
        VALUES (%s, %s, %s);"
        
    for elem in clnvi_list:
        record = (elem['val1'], elem['val2'], info_id)
        insert_into_db(conn, query, record)


def insert_into_clndn(conn, val_list, key, info_id):
    try:
        query = f"insert into {key} ({key}_GENE_SYMBOL, {key}_GENE_ID, INFO_ID) \
                VALUES (%s, %s, %s)"
        
        for elem in val_list:
            record = (elem[f"{key}_GENE_SYMBOL"], elem[f"{key}_GENE_ID"], info_id)
            insert_into_db(conn, query, record)

    except Exception as err:
        err_handler(err)


def insert_info_to_db(info_str, conn):
    
    try:
        info_list = info_str.split(";")

        info_cols = dict(
            ALLELEID='',
            CLNHGVS='',
            CLNVC='',
            CLNVCSO='',
            ORIGIN='',
            AF_ESP='',
            AF_EXAC='',
            AF_TGP='', 
            DBVARID='',
            RS='', 
            SSR='',
            )
        
        other_data = dict(
            CLNDISDB=[],
            GENEINFO=[],
            CLNVI=[],
            MC=[],
            CLNSIG=[],
            CLNSIGCONF=[],
            CLNSIGINCL=[],
            CLNDN=[],
            CLNDNINCL=[],
            CLNREVSTAT=[]
        )

        for item in info_list:
            item_data = item.split("=")
            key = item_data[0]
            val = item_data[1]
            if check_value(key):
                if key in info_cols:
                    info_cols[key] = val

                elif key in other_data:
                    other_data = insert_into_sub_tables(key, val, other_data)

        info_id_int = insert_into_info_table(conn, info_cols)
        info_id = str(info_id_int)
        if len(other_data["CLNDISDB"]) != 0: insert_into_clndisdb(conn, other_data["CLNDISDB"], info_id)
        if len(other_data["GENEINFO"]) != 0: insert_into_GENEINFO(conn, other_data["GENEINFO"], info_id)
        if len(other_data["CLNVI"]) != 0: insert_into_CLNVI(conn, other_data["CLNVI"], info_id)
        if len(other_data["CLNDNINCL"]) != 0: insert_into_clndn(conn, other_data["CLNDNINCL"], info_id)
        if len(other_data["CLNDN"]) != 0: insert_into_clndn(conn, other_data["CLNDN"], info_id)
        if len(other_data["CLNREVSTAT"]) != 0: insert_into_clnrevstat(conn, other_data["CLNREVSTAT"], info_id)
        if len(other_data["MC"]) != 0: insert_into_MC(conn, other_data["MC"], info_id)
        
        for tbl_name in ["CLNSIGINCL", "CLNSIGCONF", "CLNSIG"]:
            if len(other_data[tbl_name]) != 0: 
                insert_clnsig(conn, other_data[tbl_name], tbl_name, info_id)
        
        return info_id

    except Exception as err:
        err_handler(err)



clndisdb_split_pattern = re.compile("[\,\|]+")
def insert_into_sub_tables(key, val, other_data):
    if check_value(val):
        if key == "CLNDISDB":
            sub_list = re.split(clndisdb_split_pattern, val)
            if len(sub_list) == 0:
                values = val.split(':')
                if len(values) == 2:
                    new_elem = dict(name=values[0],  abbrv=None, id=values[1])
                elif len(values) == 3: 
                    new_elem = dict(name=values[0], abbrv=values[1], id=values[2])
                else: 
                    new_elem = dict(name=values, abbrv=None, id=None)

                other_data[key].append(new_elem)
            else:
                for sub_str in sub_list:
                    if check_value(sub_str) and sub_str != ".":
                        values = sub_str.split(':')
                        if len(values) == 2:
                            new_elem = dict(name=values[0],  abbrv=None, id=values[1])
                        elif len(values) == 3: 
                            new_elem = dict(name=values[0], abbrv=values[1], id=values[2])
                        else: 
                            new_elem = dict(name=values, abbrv=None, id=None)

                        other_data[key].append(new_elem)
        elif key == "GENEINFO" or key == "CLNVI":
            for sub_str in val.split('|'):
                if check_value(sub_str):
                    values = sub_str.split(':')
                    if len(values) == 2:
                        new_elem = dict(val1=values[0], val2=values[1])
                    else: new_elem = dict(val1=values[0], val2='')
                    other_data[key].append(new_elem)

        elif key == "MC":
            for sub_str in val.split(','):
                if check_value(sub_str):
                    sequence_ontology_id, molecular_consequence = sub_str.split('|')
                    new_mc = dict(sequence_ontology_id=sequence_ontology_id, molecular_consequence=molecular_consequence)
                    other_data[key].append(new_mc)

        elif key == "CLNREVSTAT":
            values =  val.split(',')
            if len(values) == 1: new_elem = dict(condition=values[0], num_of_submitters='', conflict='')
            elif len(values) == 2: new_elem = dict(condition=values[0], num_of_submitters=values[1], conflict='')
            elif len(values) == 3: new_elem = dict(condition=values[0], num_of_submitters=values[1], conflict=values[2])
            else:
                new_elem = values
                print(len(values))
                print(new_elem, "CLNREVSTAT")

            other_data[key].append(new_elem)
        
        elif key == "CLNSIG" or key=="CLNSIGCONF" or key=="CLNSIGINCL":
            for sub_str in val.split('|'):
                other_data[key].append(sub_str)
                    
    elif key == "CLNDN" or key=="CLNDNINCL":
                    
        GENE_SYMBOL = None
        GENE_ID = None
        for pair in val.split("|"):
            values = pair.split(":")
            if len(values) == 1: 
                GENE_SYMBOL = pair 
            else: 
                GENE_SYMBOL = values[0]
                GENE_ID = values[1]

            new_dict = {
                f"{key}_GENE_SYMBOL":GENE_SYMBOL,
                f"{key}_GENE_ID":GENE_ID,
            }
            other_data[key].append(new_dict)
            
    else: print("unexpected key", key)
    return other_data

def import_clinvar_data(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    vcf_path = f'{cwd}\\temp\\clinvar_variants.csv'

    t_0 = timeit.default_timer()
    df = pd.read_csv(vcf_path) 
    t_1 = timeit.default_timer()

    elapsed_time = round((t_1 - t_0) * 10 ** 9, 3)

    print(f"vcf file is read in {elapsed_time} ms")

    df['INFO_ID'] = df['INFO'].progress_apply(insert_info_to_db, conn=conn)

    df_t = df.drop(columns=["INFO"])
    df_t.to_csv("temp\\clinvar_variants.csv", index=False)

    t_0 = timeit.default_timer()

    insert_csv(conn, "temp\\clinvar_variants.csv", "variant", "CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO_ID")

    t_1 = timeit.default_timer()

    elapsed_time = round((t_1 - t_0) * 10 ** 3, 3)

    print(f"csv file is inserted in {elapsed_time} ms")
