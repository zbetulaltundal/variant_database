# This script imports data from clingen to database
# Zeynep Betül Altundal
import os
import pandas as pd
import sys
import psycopg2 as psql
import clingen_db_config

def db_connect():
    try:
        conn = psql.connect(
            host=clingen_db_config.DB_HOST,
            database=clingen_db_config.DB_NAME,
            user=clingen_db_config.DB_USER,
            password=clingen_db_config.DB_PWD)

        print("Database connected successfully")
        return conn
    except:
        print("Database not connected successfully")
        sys.exit()


def insert_into_db(conn, query, record):
    try:
        cur = conn.cursor()
        cur.execute(query, record)
        cur.close()
        conn.commit()
    except Exception:
        print ("Exception has occured:", Exception)
        print ("Exception type:", type(Exception))
        conn.rollback()

def import_clingen_data(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    csv_path = f'{cwd}\\data\\ClinGen'
    csv_name = 'Clingen-Gene-Disease-Summary-2022-07-22.csv'

    # using pandas read_csv function convert the data to a pandas dataframe
    data = pd.read_csv(f'{csv_path}\\{csv_name}') 

    for row in data.itertuples(): 
        if row[0] > 4:
            gene_symbol = row[1] if not pd.isna(row[1]) else None
            hgnc_id = row[2] if not pd.isna(row[2]) else None
            disease_label = row[3] if not pd.isna(row[3]) else None
            mondo_disease_id = row[4] if not pd.isna(row[4]) else None
            moi = row[5] if not pd.isna(row[5]) else None
            sop = row[6] if not pd.isna(row[6]) else None
            classification = row[7] if not pd.isna(row[7]) else None
            online_report_url = row[8] if not pd.isna(row[8]) else None
            classification_date = row[9] if not pd.isna(row[9]) else None
            gcep = row[10] if not pd.isna(row[10]) else None
            
            # data formatting
            # convert iso 8601 date format to psql timestamptz format
            if not classification_date == None: 
                # iso 8601 yy-mm-ddThh:mm:ss.mssZ
                # timestamptz yy-mm-dd hh:mm:ss+00 
                date, time = classification_date.split("T", 1)
                f_classification_date = f'{date} {time[:11]}+00'

            # convert HGNC:XXXXX TO XXXXX
            if not hgnc_id == None: f_hgnc_id = hgnc_id[5:]
            else: f_hgnc_id = None
            
            # convert MONDO:XXXXXXX TO XXXXXXX
            if not mondo_disease_id == None: f_mondo_disease_id = mondo_disease_id[6:]
            else: f_mondo_disease_id = None

            # if no classification information given, set the field to 'None'
            if classification == "No Known Disease Relationship": classification = None

            # insert record into the clingen_variants table
            query = """INSERT INTO clingen_variants (GENE_SYMBOL, HGNC_ID, DISEASE_LABEL, \
                            MONDO_DISEASE_ID, MOI, SOP, CLASSIFICATION,\
                            ONLINE_REPORT, CLASSIFICATION_DATE, GCEP)\
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            record = (gene_symbol, f_hgnc_id, disease_label, f_mondo_disease_id, \
                        moi, sop, classification, online_report_url, \
                        f_classification_date, gcep)
            
            insert_into_db(conn, query, record)


if __name__ == "__main__":
    
    conn = db_connect()

    import_clingen_data(conn)
    
    if conn:
        conn.close()
        