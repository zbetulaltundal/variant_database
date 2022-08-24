import io
import sys
from os import error
from werkzeug.utils import redirect, secure_filename
import config
from flask import render_template, request, flash, url_for
from main import psql, err_handler, check_var, listToString
import vcf 
import numpy as np
import pandas as pd

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

id_cols =  ['CHROM', 'POS', 'REF', 'ALT']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# home page
def home_page():
    return render_template("home.html")

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

    data = file.stream.read()
    stream = io.StringIO(data.decode("UTF8"), newline=None)
    vcf_reader = vcf.Reader(stream)
    variants_arr = []
    for rec in vcf_reader:
        new_row = [check_var(rec.CHROM), check_var(rec.POS), check_var(rec.REF), check_var(listToString(rec.ALT))]
        variants_arr.append(new_row)
    
    variants_df = pd.DataFrame(variants_arr, columns=id_cols)
    return variants_df

def variant_info():
    return render_template('variant-info.html')
   
def record_cmpr(row, prev_rec):
    if row != None and prev_rec != None:
        row_id = (row[1], row[2], row[4], row[5])
        prev_rec_id = (prev_rec[1], prev_rec[2], prev_rec[4], prev_rec[5])
        if row_id == prev_rec_id:
            return True
    elif row == prev_rec: return True
    
    return False


def fetch_from_db(db_name, cols, where):

    select = "SELECT * "
    fr = f"FROM {db_name}_variants "

    try:
        query = select + fr + where
        conn = psql.connect(
            host=config.HOST_NAME,
            port=config.PORT_NAME,
            database=db_name,
            user=config.DB_USER,
            password=config.DB_PWD
            )
        cur = conn.cursor() 
        cur.execute(query)
        #print(cur.mogrify(query))
        res = cur.fetchall()
        cur.close()
        conn.commit()
        variants = np.empty([1, len(cols)])
        prev_rec = None
        for row in res:
            if record_cmpr(row, prev_rec) == False:
                newRow = np.array(row[1:])
                variants = np.vstack([variants, newRow])
            
            prev_rec = row

        variants = np.delete(variants, 0, 0)
        variants_df = pd.DataFrame(variants, columns=[cols, ])
    
        return variants_df

    except Exception as err:
        err_handler(err)
        conn.rollback()
        return None

def fetch_from_clinvar(where, cols):
    select = "SELECT *"
    fr = "FROM variant"

    try:
        query = select + fr + where
        conn = psql.connect(
            host=config.HOST_NAME,
            port=config.PORT_NAME,
            database='clinvar',
            user=config.DB_USER,
            password=config.DB_PWD
            )
        cur = conn.cursor() 
        cur.execute(query)
        #print(cur.mogrify(query))
        res = cur.fetchall()
        cur.close()
        conn.commit()
        variants = np.empty([1, len(cols)])
        prev_rec = None
        for row in res:
            if record_cmpr(row, prev_rec) == False:
                newRow = np.array(row[1:])
                variants = np.vstack([variants, newRow])
            
            prev_rec = row

        variants = np.delete(variants, 0, 0)
        variants_df = pd.DataFrame(variants, cols)
    
        return variants_df

    except Exception as err:
        err_handler(err)
        conn.rollback()
        return None

def get_variant_data(df):

    civic_data = np.empty([1, 43])

    for index, row in df.iterrows():
            CHROM = row['CHROM']
            ALT = row['ALT']
            REF = row['REF']
            POS = row['POS']

            # select = "SELECT (CHROM ,  POS ,  VAR_ID ,  REF ,  ALT ,  QUAL ,  FILTER ,\
            #              GN ,  VT ,  Allele ,  Consequence ,  SYMBOL ,  Entrez_Gene_ID ,  Feature_type ,  Feature ,  HGVSc , \
            #              HGVSp ,  CIViC_Var_Name ,  CIViC_Var_ID ,  CIViC_Var_Aliases ,  CIViC_HGVS , \
            #              Allele_Registry_ID ,  ClinVar_ID ,  CIViC_Var_Ev_Score ,  CIViC_Ent_Type , \
            #              CIViC_Ent_ID ,  CIViC_Ent_URL ,  CIViC_Ent_Src ,  CIViC_Ent_Var_Origin ,\
            #              CIViC_Ent_Stat ,  CIViC_Clin_Sig ,  CIViC_Ent_Dir , \
            #              CIViC_Ent_Disease ,  CIViC_Ent_Drugs ,  CIViC_Ent_Drug_Int , \
            #              CIViC_Ev_Phenotypes ,  CIViC_Ev_Level ,  CIViC_Ev_Rating , \
            #              CIViC_Assertion_ACMG_Codes ,  CIViC_Assertion_AMP_Cat ,\
            #              CIViC_Assertion_NCCN_Guid ,  CIViC_Assertion_Regu_Appr_Guid ,\
            #              CIViC_Assertion_FDA_Comp_Test_Guid)"
            
            where = f"""WHERE ALT='{ALT}' AND\
                    REF='{REF}' AND\
                    POS='{POS}' AND\
                    CHROM='{CHROM}'"""

            new_civic_data = fetch_from_db("civic", civic_cols, where)

            #new_clingen_data = fetch_from_db("clingen", clingen_cols, where)
            # clinvar_data = fetch_from_clinvar(where)

            civic_data = np.vstack([civic_data, new_civic_data])
            #clingen_data = np.vstack([clingen_data, new_clingen_data])
            

    #var_infos_df = pd.DataFrame([civic_data, clingen_data], columns=[civic_cols, clingen_cols])
    civic_data = np.delete(civic_data, 0, 0)
    var_infos_df = pd.DataFrame(civic_data, columns=civic_cols)

    return var_infos_df

def upload_vcf_file():
    try:
        if request.method == 'POST':
            file = request.files['vcf_file']
            if file.filename == '':
                flash('Please select a file')
            elif file and allowed_file(file.filename):
                var_list = vcf_to_df(file) # converts FileStorage data to vcf record
                fetched_data = get_variant_data(var_list)
                print(fetched_data)
                flash('File uploaded succesfully')
                print("column_names")
                print(fetched_data.columns.values)
                return render_template('variant-info.html',  column_names=fetched_data.columns.values, row_data=list(fetched_data.values.tolist()), zip=zip)
            else:
                flash('Only vcf files are allowed')
        
        return render_template('home.html')

    except Exception as err:
        err_handler(err)
        return render_template('home.html')
