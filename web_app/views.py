import io
import config
from flask import Blueprint, render_template, request, flash
import psycopg2 as psql
from common_funcs import *
import numpy as np
import pandas as pd
import custom_error_handling
from main import app
import os
import allel
import time

# ********* global variables *********

clingen_cols = ['GENE_SYMBOL', 'HGNC_ID', 'DISEASE_LABEL', 'MONDO_DISEASE_ID', 
    'MOI', 'SOP', 'CLASSIFICATION', 'ONLINE_REPORT', 'CLASSIFICATION_DATE', 'GCEP']

# exclude CIViC_Var_Name,GN
civic_cols = ['CHROM' ,  'POS' ,  'VAR_ID' ,  'REF' ,  'ALT' , 'QUAL', 'FILTER', 'GN', 'VT', 'Allele', 'Consequence', 'SYMBOL', 
        'Entrez_Gene_ID', 'Feature_type', 'Feature', 'HGVSc', 'HGVSp', 'CIViC_Var_Name', 'CIViC_Var_ID', 'CIViC_Var_Aliases', 
        'CIViC_HGVS', 'Allele_Registry_ID', 'ClinVar_ID', 'CIViC_Var_Ev_Score', 'CIViC_Ent_Type', 
        'CIViC_Ent_ID', 'CIViC_Ent_URL', 'CIViC_Ent_Src', 'CIViC_Ent_Var_Origin', 'CIViC_Ent_Stat',
        'CIViC_Clin_Sig', 'CIViC_Ent_Dir', 'CIViC_Ent_Disease', 'CIViC_Ent_Drugs', 'CIViC_Ent_Drug_Int', 
        'CIViC_Ev_Phenotypes', 'CIViC_Ev_Level', 'CIViC_Ev_Rating', 'CIViC_Assertion_ACMG_Codes',
        'CIViC_Assertion_AMP_Cat', 'CIViC_Assertion_NCCN_Guid', 'CIViC_Assertion_Regu_Appr_Guid', 
        'CIViC_Assertion_FDA_Comp_Test_Guid']

pharmgkb_cols = ["Clinical_Annotation_ID", "VARIANT", "GENE", "LEVEL_OF_EVIDENCE", "LEVEL_OVERRIDE",
             "LEVEL_MODIFIERS", "SCORE", "PHENOTYPE_CATEGORY", "PMID_COUNT", "EVIDENCE_COUNT",
             "LATEST_HISTORY_DATE", "pharmgkb_URL", "Specialty_Population", "Genotype",
             "ANNOTATION_TEXT", "Allele_Function", "Evidence_ID", "Evidence_Type", "Evidence_URL", 
             "Evidence_PMID", "Evidence_Summary", "Evidence_Score"]


pharmgkb_col_name_mapper = {"GENE":"HGNC GENE SYMBOL", "LEVEL_OF_EVIDENCE": "EVIDENCE LEVEL"}
civic_col_name_mapper = {'gn': 'HGNC GENE SYMBOL', 'vt': 'CIViC Variant Name', 'entrez_gene_id': 'Entrez Gene ID', 'feature_type': 'CIViC Feature Type', 'civic_var_name': 'CIViC Variant Name', 'civic_var_id': 'CIViC Variant ID', 'civic_var_aliases': 'CIViC Variant Aliases', 'civic_hgvs': 'CIViC HGVS', 'allele_registry_id': 'CIViC Allele Registry ID', 'clinvar_id': 'ClinVar ID', 'civic_var_ev_score': 'CIViC Variant Evidence Score', 'civic_ent_type': 'CIViC Entity Type', 'civic_ent_id': 'CIViC Entity ID', 'civic_ent_url': 'CIViC Entity URL', 'civic_ent_src': 'CIViC Entity Source', 'civic_ent_var_origin': 'CIViC Entity Variant Origin', 'civic_ent_stat': 'CIViC Entity Status', 'civic_clin_sig': 'CIViC Entity Clinical Significance', 'civic_ent_dir': 'CIViC Entity Direction supports', 'civic_ent_disease': 'CIViC Entity Disease', 'civic_ent_drugs': 'CIViC Entity Drugs', 'civic_ent_drug_int': 'CIViC Entity Drug Interaction Type', 'civic_ev_phenotypes': 'CIViC Evidence Phenotypes', 'civic_ev_level': 'CIViC Evidence Level', 'civic_ev_rating': 'CIViC Evidence Rating', 
                        'civic_assertion_acmg_codes': 'CIViC Assertion ACMG Codes', 'civic_assertion_amp_cat': 'CIViC Assertion AMP Category', 'civic_assertion_nccn_guid': 'CIViC Assertion AMP Category', 'civic_assertion_regu_appr_guid': 'CIVIC Assertion Regulatory Approval', 'civic_assertion_fda_comp_test_guid': 'CIVIC Assertion FDA Companion Test'}
clingen_col_name_mapper = {"gene_symbol":"HGNC GENE SYMBOL", "gene_id": "HGNC GENE ID", "disease_label": "DISEASE LABEL",
                        "CLASSIFICATION":"CLINGEN CLASSIFICATION", "disease_id":"MONDO disease id",
                        "online_report":"CLINGEN URL", "classification_date":"CLINGEN CLASSIFICATION DATE"}


id_cols =  ['CHROM', 'POS', 'REF', 'ALT']

# ***************************

# ********* classes *********

# ***************************

bp1 = Blueprint('main_bp', __name__, url_prefix='/')

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

def select_all_from_civic(where):

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

def data_to_df(data, cols):

    data = np.delete(data, 0, 0)
    if data is None or data.size == 0:
        return None

    return np_arr_to_df(data, cols)



def join_data_frames(data_frames, join_cols):
    try:
        first_iter = True
        df1 = data_frames[0]
        for df2 in data_frames:
            if first_iter == False:
                if (df1 is None and df2 is not None) or (df1.empty and df1.empty == False): 
                    df1 = df2
                elif (df2 is None and df1 is not None) or (df2.empty and df1.empty == False): continue
                elif df1 is None and df2 is None: continue
                elif df1.empty and df2.empty: continue
                elif (df1 is not None) and (df2 is not None) and (df1.empty == False) and (df2.empty == False):
                    print(df1.columns)   
                    df1 = pd.merge(df1, df2, on=join_cols, how='outer') 

                print(df1)
                if df1 is not None: print(df1.empty)

            first_iter = False
        
        print(df1)
        print("df merged")
        return df1

    except Exception as err:
        custom_error_handling.err_handler(err)

def get_civic_data(input_vcf_df):
    civic_data = np.empty([1, len(civic_cols)])
    try:
        for index, row in input_vcf_df.iterrows():

                CHROM = row['CHROM']
                ALT = row['ALT']
                REF = row['REF']
                POS = row['POS']
                
                where = f""" WHERE ALT='{ALT}' AND\
                        REF='{REF}' AND\
                        POS='{POS}' AND\
                        CHROM='{CHROM}' """

                civic_data = np.vstack([civic_data, select_all_from_civic(where)])

        civic_df = data_to_df(civic_data, civic_cols)
        civic_df.drop(columns=['VAR_ID', 'SYMBOL', 'FILTER'], inplace=True)
        civic_df.rename(columns = civic_col_name_mapper, inplace = True)
        return civic_df
    except Exception as err:
        err_handler(err)
        return None
 


# def get_pharmgkb_data(hgnc_gene_symbol):


# def 

# def collect_data(input_vcf_df):
#     civic_df = get_civic_data(input_vcf_df)
#     civic_data = get_civic_data(input_vcf_df)
#     clingen_data = get_clingen_data(hgnc_gene_symbol)
#     pharmgkb_data = get_pharmgkb_data(hgnc_gene_symbol)
    
#     print(fetched_data)
#     flash('File uploaded succesfully')
#     #return render_template('home.html')
#     return render_template('results.html', 
#     hgnc_id=
#     civic_df=civic_df
#     column_names=fetched_data.columns.values, 
#     row_data=list(fetched_data.values.tolist()), 
#     zip=zip)

def fetch_from_civic_df(chrom, alt, ref, pos):
    try:
        where = f""" WHERE ALT='{alt}' AND\
                REF='{ref}' AND\
                POS='{pos}' AND\
                CHROM='{chrom}' """

        conn = db_connect('civic')
        civic_q = f"""SELECT CHROM ,  POS ,  VAR_ID ,  REF ,  ALT , QUAL, FILTER, GN, VT, Allele, Consequence, SYMBOL, 
            Entrez_Gene_ID, Feature_type, Feature, HGVSc, HGVSp, CIViC_Var_Name, CIViC_Var_ID, CIViC_Var_Aliases, 
            CIViC_HGVS, Allele_Registry_ID, ClinVar_ID, CIViC_Var_Ev_Score, CIViC_Ent_Type, 
            CIViC_Ent_ID, CIViC_Ent_URL, CIViC_Ent_Src, CIViC_Ent_Var_Origin, CIViC_Ent_Stat,
            CIViC_Clin_Sig, CIViC_Ent_Dir, CIViC_Ent_Disease, CIViC_Ent_Drugs, CIViC_Ent_Drug_Int, 
            CIViC_Ev_Phenotypes, CIViC_Ev_Level, CIViC_Ev_Rating, CIViC_Assertion_ACMG_Codes,
            CIViC_Assertion_AMP_Cat, CIViC_Assertion_NCCN_Guid, CIViC_Assertion_Regu_Appr_Guid, 
            CIViC_Assertion_FDA_Comp_Test_Guid FROM civic_variants {where}"""   
        civic_df = pd.read_sql_query(civic_q, con=conn)
        civic_df.drop(columns=['var_id', 'symbol', 'filter'], inplace=True)
        civic_df.rename(columns = civic_col_name_mapper, inplace = True)
        return civic_df
    except Exception as err:
        err_handler(err)
        return render_template('home.html')

def fetch_from_psql_db_df(conn, query, col_mapper, drop_cols=None):

    try:
        df = pd.read_sql_query(query, con=conn)
        if drop_cols is not None:
            df.drop(columns=drop_cols, inplace=True)
        df.rename(columns = col_mapper, inplace = True)
        return df
    
    except Exception as err:
        err_handler(err)
        return render_template('home.html')


def fetch_from_clingen(hgnc_gene_symbol):
    
    conn = db_connect('clingen') 
    where = f""" WHERE GENE_SYMBOL='{hgnc_gene_symbol}' """
    return fetch_from_psql_db_df(conn, f"""SELECT * FROM clingen_variants {where}""", clingen_col_name_mapper)
        
def fetch_from_pharmgkb(hgnc_gene_symbol):
    try:
        conn = db_connect('pharmgkb') 
        where = f""" WHERE GENE='{hgnc_gene_symbol}' """
        pharmgkb_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM pharmgkb {where}""", pharmgkb_col_name_mapper)
        # drugs_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM drug {where}""", pharmgkb_col_name_mapper)
        # phenotype_df = fetch_from_psql_db_df(conn,f"""SELECT * FROM phenotype {where}""", pharmgkb_col_name_mapper)

        #merged = join_data_frames(data_frames, "", join_type)
        return pharmgkb_df
    except Exception as err:
        err_handler(err)
        return render_template('home.html')

def check_df_empty_or_none(df):
    if df is None: return False
    if df.empty: return False

    return True

def variant_details(chrom, pos, alt, ref):
    try:
        # tüm özellikleri listele, bir kısmını topluca yukarda, 
        # bazılarını dblere göre kategorize edip aşağıda
        civic_df = fetch_from_civic_df(chrom, alt, ref, pos)
        civic_df_flag = check_df_empty_or_none(civic_df)

        print(civic_df.columns)

        hgnc_gene_symbol = civic_df.loc[0]['HGNC GENE SYMBOL']
        clingen_df = fetch_from_clingen(hgnc_gene_symbol)
        clingen_flag = check_df_empty_or_none(clingen_df)
        pharmgkb_df = fetch_from_pharmgkb(hgnc_gene_symbol)
        pharmgkb_flag = check_df_empty_or_none(pharmgkb_df)
        print(clingen_df.columns)
        print(pharmgkb_df.columns)

        df_list = [civic_df, clingen_df, pharmgkb_df]
        table_df = join_data_frames(df_list, ['HGNC GENE SYMBOL'])
        return render_template('variant-details.html',
            civic=civic_df, 
            clingen=clingen_df, 
            clingen_flag=clingen_flag,
            civic_df_flag=civic_df_flag,
            pharmgkb_flag=pharmgkb_flag,
            pharmgkb=pharmgkb_df, 
            column_names=table_df.columns,
            table_df=table_df, zip=zip)

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

    
# def filter_civic(df):
#     civic_df = fetch_from_civic_df(chrom, alt, ref, pos)
#     civic_df_flag = check_df_empty_or_none(civic_df)


def list_results(df):
    try:
        out_arr = []

        # for each record in given vcf file send queries to each db and ger results in df format
        # civic_df = filter_civic(df)
        # clinvar_df = filter_clinvar(df)

        # merge results 
        
        # send them to page

        conn = db_connect('civic')
        # input_vcf_df.apply(filter_db)
        # for index, row in input_vcf_df.iterrows():

        #     CHROM = row['CHROM']
        #     ALT = row['ALT']
        #     REF = row['REF']
        #     POS = row['POS']
            
        #     where = f""" WHERE ALT='{ALT}' AND\
        #             REF='{REF}' AND\
        #             POS='{POS}' AND\
        #             CHROM='{CHROM}' """
                
        #     query = f"SELECT GN FROM civic_variants {where};"
        #     cur = conn.cursor() 
        #     cur.execute(query)
        #     hgnc_symbol = cur.fetchone()
        #     cur.close()
        #     conn.commit()
            
        #     elem = dict(
        #         hgnc_symbol=hgnc_symbol,
        #         chrom=CHROM,
        #         alt=ALT,
        #         ref=REF,
        #         pos=POS,
        #     )

        #     print(elem)

        #     out_arr.append(elem)

        return render_template('results.html', results=out_arr)
    
    except Exception as err:
        err_handler(err)
        return render_template('home.html')


@bp1.route('/', methods=["GET", "POST"])
@bp1.route('/anasayfa', methods=["GET", "POST"])
def upload_vcf_file():
    try:
        print("in upload_vcf_file")
        if request.method == 'POST':
            file = request.files['vcf_file']
            if file.filename == '':
                flash('Please select a file')
            elif file and allowed_file(file.filename):
                content = file.read() 
                if(content == b''b''):
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                    return render_template("home.htmll")
                file_content = content.decode("utf-8")
                input_vcf_df = read_vcf_from_str(file_content)
                if input_vcf_df is None:  
                    flash('Uploaded file is empty.')
                else:
                    return list_results(input_vcf_df)
            else:
                flash('Only vcf files are allowed')
        
        return render_template('home.html')

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

# view functions for rendering html pages

def home_page():
    print("in home_page")
    return render_template("home.html")


def add_data_page():
    print("in add_data page")
    return render_template("veri-ekle.html")

def insert_data(df):
    try:
        cwd = os.getcwd()
        fpath=f'{cwd}\\Temp\\inserted.csv'
        df.to_csv(fpath, index=False)
        conn = db_connect(config.USER_DB_NAME)
        cur = conn.cursor()
        query = f'''COPY VARIANT(CHROM,POS,VAR_ID,REF,ALT,QUAL,FILTER,INFO)
            FROM '{fpath}'
            DELIMITER ','
            CSV HEADER; '''
        cur.execute(query)
        conn.commit()
        conn.close()
        flash('Dosya başarıyla veritabanına eklendi.')
        return render_template("veri-ekle.html")
    except Exception as err:
        err_handler(err)
        conn.rollback()
        conn.close()
        return render_template("veri-ekle.html")

@bp1.route('/veri-ekle', methods=["GET", "POST"])
def add_data():
    try:
        print("in add_data")
        if request.method == 'POST':
            file = request.files['insert_vcf_file']
            if file.filename == '':
                flash('Lütfen bir dosya seçiniz.')
                return render_template("veri-ekle.html")
            elif file and allowed_file(file.filename):
                content = file.stream.read() 
                if(content == b''b''):
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                    return render_template("veri-ekle.html")
                
                file_content = content.decode("utf-8")
                input_vcf_df = read_vcf_from_str(file_content)
                if input_vcf_df is None:  
                    flash('Yüklediğiniz dosyada veri bulunamadı')
                    return render_template("veri-ekle.html")
                return insert_data(input_vcf_df)
            else:
                flash('Lütfen VCF uzantılı bir dosya yükleyin.')
                return render_template("veri-ekle.html")
        else: return render_template("veri-ekle.html")
    except Exception as err:
        err_handler(err)
        return render_template("veri-ekle.html")

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


app.register_blueprint(bp1)