from asyncio.windows_events import NULL
from tqdm import tqdm
import sys
import os
import re
from common_functions import db_connect, err_handler, check_value, insert_into_db, insert_into_db_returning_id_V1
import io
import os
import pandas as pd
from db_config import CLINVAR_DB_NAME

def insert_csv():
    try:
        conn = db_connect(CLINVAR_DB_NAME)
        cwd = os.getcwd()
        fpath = f'{cwd}\\temp\\clinvar_variants_v1.csv'
        cur = conn.cursor()
        query = f'''COPY VARIANT(CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO_ID)
            FROM '{fpath}'
            DELIMITER ','
            CSV HEADER; '''

        cur.execute(query)
        conn.commit()
    except Exception as err:
        print("in function  insert csv")
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

insert_csv()
