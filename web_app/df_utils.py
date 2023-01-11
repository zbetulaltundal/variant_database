import io
import numpy as np
import pandas as pd

# custom modules

from custom_error_handling import err_handler

def np_arr_to_df(np_arr, headers):
    """ Converts given numpy array to pandas dataframe with given headers
    If fiven array is empty, creates a dataframe filled with None values
    / Numpy array'i verilen headerları kullanarak pandas dataframe'e dönüştürür
    Eğer verilen array boş ise, None değerleriyle doldurulmuş bir pandas dataframe döner

    Parameters / Parametreler
    ----------
    np_arr : numpy.array
        The numpy array

    Returns / Dönüş değeri
    -------
    df
        dataframe
        / pandas dataframe formatındaki veri
    """
    if np_arr.size == 0:
        filled_arr = np.full([1, len(headers)], None)
        df = pd.DataFrame(filled_arr, columns=headers)
    else:
        df = pd.DataFrame(np_arr, columns=headers)
    
    return df

def join_data_frames(data_frames, join_cols):
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
                    print(df1.columns)   
                    df1 = pd.merge(df1, df2, on=join_cols, how='outer') 

                print(df1)
                if check_df(df1): print(df1.empty)

            first_iter = False
        
        print(df1)
        print("df merged")
        return df1

    except Exception as err:
        err_handler(err)

def data_to_df(data, cols):

    data = np.delete(data, 0, 0)
    if data is None or data.size == 0:
        return None

    return np_arr_to_df(data, cols)


def check_df(df):
    "returns true for valid df"
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

