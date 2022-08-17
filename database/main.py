# @author: Zeynep Betül Altundal

from asyncio.windows_events import NULL
from pydoc import cli
import pandas as pd
import clingen_import
import civic_import
import clinvar_import
import db_config
import psycopg2 as psql
import sys
from collections.abc import Iterable

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
    try:
        cur = conn.cursor() 
        cur.execute(query, record)
        cur.close()
        conn.commit()
    except Exception as err:
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


# veritabanına verilen record'u verilen query ile insert eder.
# insert edilen yeni satırın id'sini döner.
def insert_into_db_returning_id(conn, query, record):
    try:
        cur = conn.cursor()
        #print(cur.mogrify(query, record))
        cur.execute(query, record)
        data = cur.fetchone()
        cur.close()
        conn.commit()
        return data[0] # id, primary key
    except Exception as err:
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

def is_iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False

# verilen değişkenin (Var) geçerli bir değere sahip olup olmadığını kontrol eden fonksiyon.
def check_var(var):
    if type(var) == list:
        if len(var) == 0: return None
        elif (len(var) == 1) and( (check_var(var[0])==None) or (var[0] == '.')): return None
        else: return var
    elif var==None or pd.isna(var) or (var  == NULL) or (var == False) or (var == 'None') or (var  == '') or (var == 'N/A'): return None
    elif is_iterable(var):
        if len(var) == 0: return None
    
    return var


# geeks4forgeeks
# Verilen list türündeki değişkeni, bir stringe dönüştürür
def listToString(list): 
    try:
        # list değişkenini kontrol eder
        if check_var(list) == None: return None
        # eğer tek bir elemandan oluşuyorsa ve tek eleman geçerli bir değere sahipse,
        # direkt birinci elemanı döner
        if len(list) == 1:
            if check_var(list[0]) == None: return None
            return list[0].sequence

        # eğer 1den fazla elemana sahip bir listeyse,

        # initialize an empty string
        # boş bir string değişkeni tanımlanır
        str1 = "" 
        
        # traverse in the string  
        # listedeki her bir eleman bu string'e eklenir
        for ele in list: 
            str1 += ele  
        
        # return string  
        # oluşan string'i döner
        return str1 

    except Exception as err:
        print ("Exception has occured:", err)
        print ("Exception type:", type(err))
        err_type, err_obj, traceback = sys.exc_info()
        line_num = traceback.tb_lineno
        # print the connect() error
        print ("\nERROR:", err, "on line number:", line_num)
        print ("traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)


# EN
# Search if the dictionary contains the field as a key.
# TR
# Verilen sözlük(dict) verilen key'ı içeriyor mu diye kontrol eder.
# Argüman olarak dict ve key'ı alır 
def search_dict(dict, key):
    if key in dict:
        val = dict[key]
        if val == '': 
            val = None
            return None
        if check_var(val): return None
        else: 
            if type(val) == list:
                if len(val) == 0: return None
                elif len(val) == 1: return val[0]
            return val
    else: return None

if __name__ == "__main__":
    
    conn = db_connect(db_config.CIVIC_DB_NAME)

    civic_import.import_civic_data(conn)
    
    if conn:
       conn.close()

    # conn = db_connect(db_config.CLINGEN_DB_NAME)

    # clingen_import.import_clingen_data(conn)
    
    # if conn:
    #    conn.close()

    # conn = db_connect(db_config.CLINVAR_DB_NAME)

    # clinvar_import.import_clinvar_data(conn)
    
    # if conn:
    #    conn.close()
        