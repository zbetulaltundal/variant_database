
import db_config
import psycopg2 as psql
import os
from zipfile import ZipFile
from utils import err_handler
from db_utils import db_connect
import db_config

def search_db(db_list, db_name):

    for val in db_list:
        if val[0] == db_name: return True 

    return False

def extract_zip(db_name):
    with ZipFile(f".\\db_backups\\{db_name}.zip", 'r') as zObject:
  
        # Extracting specific file in the zip
        # into a specific location.
        zObject.extract(
            f"{db_name}.sql", path=".\\temp")
    zObject.close()


if __name__ == "__main__":
    
    conn = None
    try:
        
        # create databases
        conn = db_connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("select datname from pg_database;")
        db_list = cur.fetchall()
    
        for db_name in db_config.DB_NAMES:
            # check if database already exists
            res = search_db(db_list, db_name)
            if res == False: 
                cur.execute(f"create database {db_name};")
            
        conn.commit()
        if conn:
            conn.close()

    except Exception as err:
        err_handler(err)

    try:
        # restore databases using backup .sql files
        for db_name in db_config.DB_NAMES: 
            extract_zip(db_name)
            os.system(f''' pg_restore --no-owner --dbname=postgresql://postgres:test@localhost:5432/{db_name} -v \
                    .\db_backups\{db_name}.sql''')

    except Exception as err:
        err_handler(err)