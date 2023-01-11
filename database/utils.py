from asyncio.windows_events import NULL
import io
import pandas as pd
import sys
import numpy as np
import os
from functools import reduce

def err_handler(err):
    print ("Exception has occured:", err)
    print ("Exception type:", type(err))
    err_type, err_obj, traceback = sys.exc_info()
    if traceback != None:
        line_num = traceback.tb_lineno
        fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
        print(f"in {fname}")
    else: line_num = "not found"
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

def is_iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


def read_vcf(path, n_rows=None):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    
    if n_rows is not None:
        return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
            'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t', nrows=n_rows
    ).rename(columns={'#CHROM': 'CHROM'})
    
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})


def check_value(val):
    '''
    checks if value field is empty, nan, None, 'nan', 'None', , or an empty string, if not, notes as error
    val: value to check
    '''
    if type(val) == list:
        if len(val) == 0: return False
        elif (len(val) == 1) and( (check_var(val[0])==None) or (val[0] == '.')): return False
        else: return True
    if isinstance(val, float) and np.isnan(val):
        return False
    if val != None and val != NULL and val and val != 'nan' and val != 'None': 
        if isinstance(val, str):
            if len(val) == 0: return False
            elif(val == '' or val =='N/A'): return False
            else: return True
        return True

    return False

def check_var(var):
    if check_value(var): return var
    return None

# geeks4forgeeks
# Verilen list türündeki değişkeni, bir stringe dönüştürür
def listToString(list): 
    try:
        # list değişkenini kontrol eder
        if check_var(list): return None
        # eğer tek bir elemandan oluşuyorsa ve tek eleman geçerli bir değere sahipse,
        # direkt birinci elemanı döner
        if len(list) == 1:
            if check_var(list[0]): return None
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
        if check_var(val) == None: return None
        else: 
            if type(val) == list:
                if len(val) == 0: return None
                elif len(val) == 1: return val[0]
                
            return val
    else: return None

def write_csv(df, path, index=False):
    if os.path.exists(path): df.to_csv(path, mode="w", index=index)
    else: df.to_csv(path, index=index)

def join_data_frames(data_frames, join_cols):

    try:
        df_merged = reduce(lambda  left,right: pd.merge(left,right, on=join_cols, how='outer'), data_frames)
        return df_merged

    except Exception as err:
        err_handler(err)

def tsv_to_df(folder_path, filename):
    try:
        full_path = folder_path + filename
        tsv_file = pd.read_csv(full_path, sep = '\t')
        return tsv_file
    except Exception as err:
        err_handler(err)
