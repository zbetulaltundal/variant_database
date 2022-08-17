import io
import sys
from os import error
from werkzeug.utils import redirect, secure_filename
import config
from flask import render_template, request, flash, url_for
import main
import vcf 
import numpy as np

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# home page
def home_page():

    conn = main.db_connect(config.CLINVAR_DB_NAME)

    try: 
        curr = conn.cursor()
        print(request)
        if request.method == 'POST':
            # return upload_vcf_file(request)
            print("post request")
        curr.close()
        conn.commit()
    except error:
        print(error)
        conn.rollback()
    finally:
        conn.close()
        return render_template("home.html")

def vcf_to_rec(file):

    data = file.stream.read()
    stream = io.StringIO(data.decode("UTF8"), newline=None)
    vcf_reader = vcf.Reader(stream)
    for rec in vcf_reader:
       return rec
    
    return None

def success_page():
    return render_template('success.html')

def index_page():
    return render_template('index.html')



# veritabanına verilen record'u verilen query ile insert eder
def fetch_from_db(conn, query):
    try:
        cur = conn.cursor() 
        cur.execute(query)
        result = cur.fetchall()
        print("variant info")
        print(result)
        # variants = np.zeros([1, 4], dtype='str')
        # for row in result:
        #     newRow = np.array(row)
        #     variants = np.vstack([variants, newRow])

        # variants = np.delete(variants, 0, 0)

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
    finally:
        return render_template('variant-info.html', variant_info=result)


def get_variant_data(rec):

    conn = main.db_connect('CIVic')

    # VARIANTS
    CHROM = main.check_var(rec.CHROM)
    POS = main.check_var(rec.POS)
    REF = main.check_var(rec.REF)
    ALT = main.check_var(main.listToString(rec.ALT))

    main.db_connect('CIVic')
    select = "SELECT (CIViC_Ent_Disease, CIViC_Ent_Drugs, CIViC_Clin_Sig)"
    fr = "FROM civic_variants"
    where = f"""civic_variants.ALT='{ALT}' AND\
        civic_variants.REF='{REF}' AND\
        civic_variants.POS='{POS}' AND\
        civic_variants.CHROM='{CHROM}'"""
    query = select + fr + where
    fetch_from_db(conn, query)

    if conn:
       conn.close()


def upload_vcf_file():
    try:
        if request.method == 'POST':
            # return upload_vcf_file(request)
            print(request.files['vcf_file'])
            file = request.files['vcf_file']
            if file and file.filename == '':
                flash('No file selected for uploading')
                return render_template("index.html")
            elif file and allowed_file(file.filename):
                rec = vcf_to_rec(file) # converts FileStorage data to vcf record
                if rec != None:
                   #fetched_data = get_variant_data(rec)
                   #print(fetched_data)
                   flash('File uploaded succesfully')
                   return render_template("success.html")
                else:
                   return render_template("index.html")
            else:
                flash('Only vcf files are allowed')
                return render_template("index.html")
        else:
            return render_template('index.html')

    except Exception as err:
        print ("Exception has occured:", err)
        print ("Exception type:", type(err))
        err_type, err_obj, traceback = sys.exc_info()
        line_num = traceback.tb_lineno
        # print the connect() error
        print ("\nERROR:", err, "on line number:", line_num)
        print ("traceback:", traceback, "-- type:", err_type)
        
        return render_template('index.html')
