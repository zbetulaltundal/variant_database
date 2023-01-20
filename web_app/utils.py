
import pandas as pd
from asyncio.windows_events import NULL
import psycopg2 as psql
import config
import sys
import os

def err_handler(err):
    print ("Exception has occured:", err)
    print ("Exception type:", type(err))
    err_type, err_obj, traceback = sys.exc_info()
    if traceback is not None: 
        fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
        line_num = traceback.tb_lineno
    else: 
        fname = "not found"
        line_num = "not found"
    print("in file:", fname)
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

def print_list(a):
    """ Prints out elements in given list to the console 
    a: a python list
    """
    for x in range(len(a)):
        print(a[x])

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


def allowed_file(filename):
    """ Checks if given file has one of the allowed extensions in app
    / Verilen dosya isminin uzantısı geçerli olan uzantılar arasında mı kontrol eder
    Parameters / Parametreler
    ----------
    filename : str
        The file name (dosya adı)

    Returns / Dönüş değeri
    -------
    a boolean value (True / False)
        returns True if file is allowed, else False
        / eğer dosya geçerliyse True, değil ise False döner
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def record_cmpr(rec1, rec2):
    """ Checks if the given records are identical or not
    using ALT, REF, POS, CHROM fields of the vcf records, returns
    true if identical 
    rec1, rec2: vcf records in format: [CHROM, POS, REF, ALT]
    """
    if rec1 != None and rec2 != None:
        rec1_id = (rec1[1], rec1[2], rec1[4], rec1[5])
        rec2_id = (rec2[1], rec2[2], rec2[4], rec2[5])
        if rec1_id == rec2_id:
            return True
    elif rec1 == rec2: return True
    
    return False

import io
from typing import Literal
import numpy as np
import pandas as pd

# custom modules

from utils import err_handler

def join_data_frames(data_frames, join_cols=[], join_type='inner'):
    try:
        first_iter = True
        df1 = data_frames[0]
        for df2 in data_frames:
            if first_iter == False:
                if check_df(df1) == False and check_df(df2): 
                    df1 = df2
                elif check_df(df2) == False and check_df(df1): continue
                elif (check_df(df1) or check_df(df2)) == False: continue
                elif check_df(df1) and check_df(df2):
                    if join_type == 'inner':df1 = pd.merge(df1, df2, on=join_cols, how="inner") 
                    elif join_type == 'outer':df1 = pd.merge(df1, df2, on=join_cols, how="outer") 
                    elif join_type == 'left':df1 = pd.merge(df1, df2, on=join_cols, how="left") 
                    elif join_type == 'right':df1 = pd.merge(df1, df2, on=join_cols, how="right") 
                    elif join_type == 'cross':df1 = pd.merge(df1, df2, on=join_cols, how="cross") 

            first_iter = False
        
        return df1

    except Exception as err:
        err_handler(err)

def check_df(df):
    # returns true for valid df
    if df is None: return False
    if df.empty: return False

    return True

def excel_to_df(path):
    try:
        return pd.read_excel(path)

    except Exception as err:
        err_handler(err)
        return None


def read_vcf_from_str(file_content):
    """ Store data in the vcf file on a pandas dataframe 
    / Vcf dosyasındaki verileri bir pandas dataframe'e depolar
    Parameters / Parametreler
    ----------
    file_content : str
        The content of vcf file (vcf dosyasının içeriği)

    Returns vcf file in the pandas dataframe format
        / pandas dataframe formatındaki vcf dosyası
    """
    try:
        lines = [l for l in io.StringIO(file_content) if not l.startswith('##')]
        return pd.read_csv(
            io.StringIO(''.join(lines)),
            dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
                'QUAL': str, 'FILTER': str, 'INFO': str},
            sep='\t'
        ).rename(columns={'#CHROM': 'CHROM'})
    except Exception as err:
        err_handler(err)
        return None

def write_csv(df, path, index=True):
    if os.path.exists(path): df.to_csv(path, mode="w", index=index)
    else: df.to_csv(path, index=index)