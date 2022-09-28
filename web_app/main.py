from flask import Flask, render_template, request, session, flash
from os import error, path
from werkzeug.utils import redirect
import config
from datetime import datetime
import psycopg2 as psql
import pandas as pd
from views import *
from asyncio.windows_events import NULL

app = Flask(__name__)

def is_iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False

def err_handler(err):
    print ("Exception has occured:", err)
    print ("Exception type:", type(err))
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

# verilen değişkenin (Var) geçerli bir değere sahip olup olmadığını kontrol eden fonksiyon.
def check_var(var):
    if type(var) == list:
        if len(var) == 0: return None
        elif (len(var) == 1) and( (check_var(var[0])==None) or (var[0] == '.')): return None
        else: return var
    if type(var) == bool:
        if var == False: return None
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
        err_handler(err)

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


if __name__ == "__main__":
    
    app.config.from_pyfile("config.py")
    # home page
    app.add_url_rule("/", view_func=home_page, methods=['GET'])
    app.add_url_rule("/terimler", view_func=dict_page, methods=['GET'])
    app.add_url_rule("/", view_func=upload_vcf_file, methods=["GET", "POST"])
    app.add_url_rule('/varyant-bilgisi', view_func=variant_info, methods=['GET' , "POST"])

    app.run(host="0.0.0.0", port=8080)

