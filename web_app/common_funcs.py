
from custom_error_handling import err_handler
import pandas as pd
from asyncio.windows_events import NULL
import config
import psycopg2 as psql

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
