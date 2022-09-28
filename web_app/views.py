import io
import sys
from os import error
from werkzeug.utils import redirect, secure_filename
import config
from flask import render_template, request, flash, url_for
from main import psql, err_handler, check_var, listToString, db_connect
import vcf 
import numpy as np
import pandas as pd

# ********* global variables *********

clingen_cols = ['GENE_SYMBOL', 'HGNC_ID', 'DISEASE_LABEL', 'MONDO_DISEASE_ID', 
    'MOI', 'SOP', 'CLASSIFICATION', 'ONLINE_REPORT', 'CLASSIFICATION_DATE', 'GCEP']

civic_cols = ['CHROM' ,  'POS' ,  'VAR_ID' ,  'REF' ,  'ALT' , 'QUAL', 'FILTER', 'GN', 'VT', 'Allele', 'Consequence', 'SYMBOL', 
        'Entrez_Gene_ID', 'Feature_type', 'Feature', 'HGVSc', 'HGVSp', 'CIViC_Var_Name', 'CIViC_Var_ID', 'CIViC_Var_Aliases', 
        'CIViC_HGVS', 'Allele_Registry_ID', 'ClinVar_ID', 'CIViC_Var_Ev_Score', 'CIViC_Ent_Type', 
        'CIViC_Ent_ID', 'CIViC_Ent_URL', 'CIViC_Ent_Src', 'CIViC_Ent_Var_Origin', 'CIViC_Ent_Stat',
        'CIViC_Clin_Sig', 'CIViC_Ent_Dir', 'CIViC_Ent_Disease', 'CIViC_Ent_Drugs', 'CIViC_Ent_Drug_Int', 
        'CIViC_Ev_Phenotypes', 'CIViC_Ev_Level', 'CIViC_Ev_Rating', 'CIViC_Assertion_ACMG_Codes',
        'CIViC_Assertion_AMP_Cat', 'CIViC_Assertion_NCCN_Guid', 'CIViC_Assertion_Regu_Appr_Guid', 
        'CIViC_Assertion_FDA_Comp_Test_Guid']

clinvar_cols = ["CHROM", "POS", "REF", "ALT", "QUAL", "FILTER", "CLINVAR_ID", "AF_ESP", "AF_TGP", "AF_EXAC", "ALLELEID", "CLNHGVS", "CLNVC", 
        "CLNVCSO", "DBVARID", "ORIGIN", "RS", "SSR", "ABBRV", "CLNDISDB_NAME", "CLNDISDB_ID", 
        "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "Mol_Conseq", "Seq_Ont_ID",
         "Gene_Sym", "Gene_ID", "STAT", "SRC", "SRC_ID", "DISEASE_NAME", "DISEASE_ID",
         "INCL_DISEASE_NAME", "INCL_DISEASE_ID"]

id_cols =  ['CHROM', 'POS', 'REF', 'ALT']


# ***************************

# ********* classes *********

class clinvar_tbl:

    # init method or constructor
    def __init__(self, name, _cols, _query):
        self.name = name
        self.cols = _cols
        self.query = _query

# ***************************

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
    using ALT, REF, POS, CHROM fields of the records
    / Verilen iki kaydın aynı olup olmadığını kontrol eder
    Bunu yaparken ALT, REF, POS, CHROM parametrelerini kullanır
    Parameters / Parametreler
    ----------
    rec1 : PyVCF Reader record
        The first record (birinci kayıt)

    rec2 : PyVCF Reader record
        The second record (ikinci kayıt)

    Returns / Dönüş değeri
    -------
    a boolean value (True / False)
        returns True if file is allowed, else False
        / eğer dosya geçerliyse True, değil ise False döner
    """
    if rec1 != None and rec2 != None:
        rec1_id = (rec1[1], rec1[2], rec1[4], rec1[5])
        rec2_id = (rec2[1], rec2[2], rec2[4], rec2[5])
        if rec1_id == rec2_id:
            return True
    elif rec1 == rec2: return True
    
    return False

def vcf_to_df(file):
    """ Store data in the vcf file on a pandas dataframe 
    / Vcf dosyasındaki verileri bir pandas dataframe'e depolar

    Parameters / Parametreler
    ----------
    file : str
        The vcf file (vcf dosyası)

    Returns / Dönüş değeri
    -------
    variants_df
        variant datas in the pandas dataframe format
        / pandas dataframe formatındaki varyant verileri
    """
    try:
        data = file.stream.read()
        stream = io.StringIO(data.decode("UTF8"), newline=None)
        vcf_reader = vcf.Reader(stream)
        variants_arr = []
        for rec in vcf_reader:
            new_row = [check_var(rec.CHROM), check_var(rec.POS), check_var(rec.REF), check_var(listToString(rec.ALT))]
            variants_arr.append(new_row)
        
        variants_df = pd.DataFrame(variants_arr, columns=id_cols)
        return variants_df

    except Exception as err:
        err_handler(err)
        print("err variants_arr:")
        print(variants_arr)
        return None

def print_list(a):
    """ Prints out elements in given list to the console 
    / Verilen listenin elemanlarını konsola bastırır

    Parameters / Parametreler
    ----------
    a : list
        Python List

    Returns / Dönüş değeri
    -------
    Void
    """
    for x in range(len(a)):
        print(a[x])

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

def fetch_from_db(conn, cols, query, flag=False):

    try:
        cur = conn.cursor() 
        cur.execute(query)
        #print(cur.mogrify(query))
        res = cur.fetchall()
        cur.close()
        conn.commit()
        data = np.empty([1, len(cols)])
        prev_rec = None
        for row in res: 
            if flag:
                if record_cmpr(row, prev_rec) == False:
                    newRow = np.array(row)
                    data = np.vstack([data, newRow])
            else:
                newRow = np.array(row)
                data = np.vstack([data, newRow])
            
            prev_rec = row

        data = np.delete(data, 0, 0)
    
        if data.size != 0:
            if data.shape[0] > 1:
                str = ""
                for elem in data:
                    for elem_str in elem:
                        str = str + elem_str + ", "

                val = np.array([[str]])
                return val

        return data

    except IndexError as err:
        print("IndexError('tuple index out of range')")
        err_handler(err)
        return None
    except Exception as err:
        err_handler(err)
        print("err data:")
        print(data)
        print("err newRow:")
        print(newRow)
        conn.rollback()
        return None

def combine_clinvar_tbl(clinvar_tbl_arr):

    res_arr = np.full([1, 0], None)
    conn = db_connect('clinvar')

    try:
        for tbl in clinvar_tbl_arr:
            if tbl.name == 'VARIANT':
                 data = fetch_from_db(conn, tbl.cols, tbl.query, True)
            else: 
                data = fetch_from_db(conn, tbl.cols, tbl.query)
            if data is not None and data.size != 0:
                res_arr = np.hstack((res_arr, data))
            else:    
                res_arr = np.hstack((res_arr, np.full([1, len(tbl.cols)], None)))
                
        return res_arr

    except Exception as err:
        err_handler(err)
        print("err res_arr:")
        print(res_arr)
        print("err data:")
        print(data)

def fetch_from_civic(where):

    conn = db_connect('civic')
    civic_q = f"""SELECT CHROM ,  POS ,  VAR_ID ,  REF ,  ALT , QUAL, FILTER, GN, VT, Allele, Consequence, SYMBOL, 
        Entrez_Gene_ID, Feature_type, Feature, HGVSc, HGVSp, CIViC_Var_Name, CIViC_Var_ID, CIViC_Var_Aliases, 
        CIViC_HGVS, Allele_Registry_ID, ClinVar_ID, CIViC_Var_Ev_Score, CIViC_Ent_Type, 
        CIViC_Ent_ID, CIViC_Ent_URL, CIViC_Ent_Src, CIViC_Ent_Var_Origin, CIViC_Ent_Stat,
        CIViC_Clin_Sig, CIViC_Ent_Dir, CIViC_Ent_Disease, CIViC_Ent_Drugs, CIViC_Ent_Drug_Int, 
        CIViC_Ev_Phenotypes, CIViC_Ev_Level, CIViC_Ev_Rating, CIViC_Assertion_ACMG_Codes,
        CIViC_Assertion_AMP_Cat, CIViC_Assertion_NCCN_Guid, CIViC_Assertion_Regu_Appr_Guid, 
        CIViC_Assertion_FDA_Comp_Test_Guid FROM civic_variants {where}"""   
    return fetch_from_db(conn, civic_cols, civic_q, True)

def fetch_from_clinvar(where):

    info_id_selector = f"WHERE INFO_ID IN (SELECT INFO_ID FROM variant {where})"
    
    variant = clinvar_tbl("VARIANT", ["CHROM", "POS", "REF", "ALT", "QUAL", "FILTER", "CLINVAR_ID"], f"select CHROM, POS, REF, ALT, QUAL, FILTER, CLINVAR_ID from variant {where};")
    info = clinvar_tbl("INFO", ["AF_ESP", "AF_TGP", "AF_EXAC", "ALLELEID", "CLNHGVS", "CLNVC", "CLNVCSO", 
        "DBVARID", "ORIGIN", "RS", "SSR"],
        f"SELECT AF_ESP, AF_TGP, AF_EXAC, ALLELEID, CLNHGVS, CLNVC, CLNVCSO, \
        DBVARID, ORIGIN, RS, SSR FROM INFO WHERE id IN (SELECT INFO_ID FROM variant {where});")
    CLNDISDB_ABBRV = clinvar_tbl("CLNDISDB_ABBRV", ["ABBRV"], f"SELECT ABBRV FROM CLNDISDB_ABBRV WHERE ID IN \
            (SELECT CLNDISDB_NAME_ID FROM CLNDISDB \
                {info_id_selector});")
    CLNDISDB = clinvar_tbl("CLNDISDB", ["CLNDISDB_NAME", "CLNDISDB_ID"], 
     f"SELECT CLNDISDB_NAME, CLNDISDB_ID FROM CLNDISDB \
            {info_id_selector};")
    CLNSIG = clinvar_tbl("CLNSIG", ["CLNSIG"], f"SELECT CLNSIG FROM CLNSIG \
            {info_id_selector};")
    CLNSIGCONF = clinvar_tbl("CLNSIGCONF", ["CLNSIGCONF"], f"SELECT CLNSIGCONF FROM CLNSIGCONF \
            {info_id_selector};")
    CLNSIGINCL = clinvar_tbl("CLNSIGINCL", ["CLNSIGINCL"], f"SELECT CLNSIGINCL FROM CLNSIGINCL \
            {info_id_selector};")
    MC = clinvar_tbl("MC", ["Mol_Conseq", "Seq_Ont_ID"], f"SELECT Mol_Conseq, Seq_Ont_ID FROM MC \
            {info_id_selector};")
    GENEINFO = clinvar_tbl("GENEINFO", ["Gene_Sym", "Gene_ID"], f"SELECT Gene_Sym, Gene_ID FROM GENEINFO \
            {info_id_selector};")
    CLNREVSTAT = clinvar_tbl("CLNREVSTAT", ["STAT"], f"SELECT STAT FROM CLNREVSTAT \
            {info_id_selector};")
    CLNVI = clinvar_tbl("CLNVI", ["SRC", "SRC_ID"], f"SELECT SRC, SRC_ID FROM CLNVI \
            {info_id_selector};")
    CLNDN = clinvar_tbl("CLNDN", ["DISEASE_NAME", "DISEASE_ID"], f"SELECT DISEASE_NAME, DISEASE_ID FROM CLNDN \
            {info_id_selector};")
    CLNDNINCL = clinvar_tbl("CLNDNINCL",["INCL_DISEASE_NAME", "INCL_DISEASE_ID"],  f"SELECT DISEASE_NAME, DISEASE_ID FROM CLNDNINCL \
            {info_id_selector};")

    clinvar_tbl_arr = [variant, info, CLNDISDB_ABBRV, CLNDISDB, CLNSIG, CLNSIGCONF, 
      CLNSIGINCL, MC, GENEINFO, CLNREVSTAT, CLNVI, CLNDN, CLNDNINCL]
    
    res_arr = combine_clinvar_tbl(clinvar_tbl_arr)

    return res_arr

def data_to_df(data, cols):

    data = np.delete(data, 0, 0)
    if data is None or data.size == 0:
        return None

    return np_arr_to_df(data, cols)

def combine_data_frames(df1, df2):
    
    if df1 is None and df2 is None:
        return None
    elif df1 is None: return df2
    elif df2 is None: return df1
    
    cols = np.intersect1d(df1.columns, df2.columns).tolist()
    return pd.merge(df1, df2, on=cols, how='outer') 

def get_variant_data(df):

    civic_data = np.empty([1, len(civic_cols)])
    clinvar_data = np.empty([1, len(clinvar_cols)])
    try:

        for index, row in df.iterrows():

                CHROM = row['CHROM']
                ALT = row['ALT']
                REF = row['REF']
                POS = row['POS']
                
                where = f""" WHERE ALT='{ALT}' AND\
                        REF='{REF}' AND\
                        POS='{POS}' AND\
                        CHROM='{CHROM}' """

                civic_data = np.vstack([civic_data, fetch_from_civic(where)])
                clinvar_data = np.vstack([clinvar_data, fetch_from_clinvar(where)])

        print("civic_data")
        print(civic_data)
        print("clinvar_data")
        print(clinvar_data)
        civic_df = data_to_df(civic_data, civic_cols)
        clinvar_df = data_to_df(clinvar_data, clinvar_cols)

        df_merged = combine_data_frames(civic_df, clinvar_df)
        print(df_merged)
        # common_cols = np.intersect1d(civic_df.columns, clinvar_df.columns).tolist()
        # df_merged = pd.merge(civic_df, clinvar_df, on=common_cols, how='outer')
        # data_frames = [civic_df, clinvar_df]
        # df_merged = combine_data_frames(data_frames)
    
        # df_merged.head()

        # return df_merged
        print("here")

        return df_merged

    except Exception as err:
        err_handler(err)
        return None

def upload_vcf_file():
    try:
        if request.method == 'POST':
            file = request.files['vcf_file']
            if file.filename == '':
                flash('Please select a file')
            elif file and allowed_file(file.filename):
                var_list = vcf_to_df(file)
                fetched_data = get_variant_data(var_list)
                print(fetched_data)
                flash('File uploaded succesfully')
                #return render_template('home.html')
                return render_template('variant-info.html',  column_names=fetched_data.columns.values, row_data=list(fetched_data.values.tolist()), zip=zip)
            else:
                flash('Only vcf files are allowed')
        
        return render_template('home.html')

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

# view functions for rendering html pages

def home_page():
    return render_template("home.html")

def variant_info():
    return render_template('variant-info.html')

def excel_to_df(path):
    try:
        return pd.read_excel(path)

    except Exception as err:
        err_handler(err)
        return None

def dict_page():
    nomenc = excel_to_df(config.DICT_EXCEL_PATH)
    if nomenc is None: isNone = True
    else: isNone = False
    return render_template('dict.html', nomenc=nomenc, isNone=isNone)