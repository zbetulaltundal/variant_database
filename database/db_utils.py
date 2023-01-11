
import db_config
import psycopg2 as psql
import sys

from utils import err_handler

# ismi verilen veritabanına bağlantıyı sağlar
def db_connect(db_name):
    try:
        conn = psql.connect(
            host=db_config.DB_HOST,
            database=db_name,
            user=db_config.DB_USER,
            password=db_config.DB_PWD)

        print("Database connected successfully")
        return conn
    except:
        print("Database not connected successfully")
        sys.exit()

# veritabanına verilen record'u verilen query ile insert eder
def insert_into_db(conn, query, record):
    cur = None
    try:
        cur = conn.cursor() 
        cur.execute(query, record)
        cur.close()
        conn.commit()
    except Exception as err:
        print(cur.mogrify(query))
        err_handler(err)
        conn.rollback()


def insert_csv(conn, fpath, tbl_name, tbl_cols=None, sep=","):
    try:
        if tbl_cols==None: 
            query = f'''COPY {tbl_name}
                FROM '{fpath}'
                DELIMITER '{sep}'
                CSV HEADER; '''
        else:
            query = f'''COPY {tbl_name}({tbl_cols})
                FROM '{fpath}'
                DELIMITER '{sep}'
                CSV HEADER; '''

        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Exception as err:
        err_handler(err)
        conn.rollback()

# veritabanına verilen record'u verilen query ile insert eder.
# insert edilen yeni satırın id'sini döner.
def insert_into_db_returning_id_V1(conn, query, record):
    try:
        cur = conn.cursor()
        # print(cur.mogrify(query, record))
        cur.execute(query, record)
        data = cur.fetchone()
        cur.close()
        conn.commit()
        return data[0] # id, primary key
    except Exception as err:
        err_handler(err)
        conn.rollback()
        return None


# veritabanına verilen record'u verilen query ile insert eder.
# insert edilen yeni satırın id'sini döner.
def insert_into_db_returning_id_V2(conn, query):
    try:
        print(query)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchone()
        cur.close()
        conn.commit()
        return data[0] # id, primary key
    except Exception as err:
        err_handler(err)
        conn.rollback()
        return None
