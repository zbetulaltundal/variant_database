
from flask import render_template, request, flash, send_file
import timeit 
import pandas as pd
import io 

# custom modules

from db_utils import(
    fetch_from_user_db,
    list_results,
    insert_data,
    fetch_variant_data
)

from utils import(
    allowed_file,
    err_handler,
    excel_to_df,
    read_vcf_from_str,
    check_df,
    write_vcf
)

import config

# VIEW FUNCTIONS

def variant_details(chrom, pos, alt, ref, hgnc=None):
    try:
        # tüm özellikleri listele, bir kısmını topluca yukarda, 
        # bazılarını dblere göre kategorize edip aşağıda 
        
        df_joined, civic_df, clinvar_df, pharmgkb_df, clingen_df,uniprot_df, user_df = fetch_variant_data(chrom, pos, ref, alt, hgnc)

        values = dict(
            chrom=chrom,
            pos=pos,
            ref=ref,
            alt=alt,
            hgnc=hgnc
        )   
        clingen_flag=check_df(clingen_df)
        civic_flag=check_df(civic_df)
        clinvar_flag=check_df(clinvar_df)
        pharmgkb_flag=check_df(pharmgkb_df)
        uniprot_flag=check_df(uniprot_df)
        user_flag=check_df(user_df)

        civic_cols = civic_df.columns if civic_flag else None
        clinvar_cols = clinvar_df.columns if clinvar_flag else None
        clingen_cols = clingen_df.columns if clingen_flag else None
        pharmgkb_cols = pharmgkb_df.columns if pharmgkb_flag else None
        clinvar_cols = clinvar_df.columns if clinvar_flag else None
        uniprot_cols = uniprot_df.columns if uniprot_flag else None
        user_cols = user_df.columns if user_flag else None

        return render_template('user-variant-details.html',
            values=values,
            civic=civic_df, clingen=clingen_df, clinvar=clinvar_df, 
            pharmgkb=pharmgkb_df, user=user_df, uniprot=uniprot_df,
            civic_cols=civic_cols, clingen_cols=clingen_cols, clinvar_cols=clinvar_cols, 
            pharmgkb_cols=pharmgkb_cols, user_cols=user_cols, uniprot_cols=uniprot_cols,
            civic_flag=civic_flag, clingen_flag=clingen_flag,clinvar_flag=clinvar_flag,
            pharmgkb_flag=pharmgkb_flag, user_flag=user_flag, uniprot_flag=uniprot_flag, zip=zip)

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

def upload_vcf_file():
    is_none = True

    try:
        if request.method == 'POST':
            file = request.files['vcf_file']
            if file.filename == '':
                flash('Lütfen bir dosya seçiniz.')
            elif file and allowed_file(file.filename):
                content = file.read() 
                if(content == b''b''): 
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                    return render_template("home.html")
                file_content = content.decode("utf-8")
                input_vcf_df = read_vcf_from_str(file_content)
                if input_vcf_df is None:  
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                else:
                    res_df = list_results(input_vcf_df)
                    is_none = not check_df(res_df)
                    if is_none == False:        
                        trimmed_results_df = res_df.head(50)
                        path = 'Temp\\results.vcf'
                        write_vcf(res_df, path)
                        cols = res_df.columns
                        mapper = dict()
                        for col in cols:
                            mapper[col] = col.replace(" ", "-")
                        
                        return render_template('results.html',
                                column_names=cols, 
                                column_names_mapper=mapper, 
                                is_none=is_none, 
                                res_df=trimmed_results_df, zip=zip)

            else:
                flash('Lütfen VCF uzantılı bir dosya yükleyin.')
        
        return render_template('results.html', res_df=None, column_names=None, is_none=True)

    except Exception as err:
        err_handler(err)
        return render_template('results.html', res_df=None, column_names=None, is_none=True)

def home_page():
    return render_template("home.html")

def add_data_page():
    return render_template("insert-data.html")

def userdb_variants():
    
    try:
        df = fetch_from_user_db()
        cols = df.columns
        mapper = dict()
        is_none = not check_df(df)
        for col in cols:
            mapper[col] = col.replace(" ", "-")
        
        return render_template('userdb.html',
                column_names=cols, 
                column_names_mapper=mapper, 
                is_none=is_none, 
                df=df, zip=zip)

    except Exception as err:
        err_handler(err)
        return render_template('userdb.html',
                column_names=None, 
                column_names_mapper=None, 
                is_none=True, 
                df=None, zip=zip)

def user_variant_details(chrom, pos, alt, ref, hgnc=None):
    try:
        # tüm özellikleri listele, bir kısmını topluca yukarda, 
        # bazılarını dblere göre kategorize edip aşağıda 
        where = f"WHERE ALT='{alt}' AND REF='{ref}' AND POS='{pos}' AND CHROM='{chrom}'"
        res = fetch_from_user_db(where)

        values = dict(
            chrom=res.loc[0]['chrom'],
            pos=res.loc[0]['pos'],
            ref=res.loc[0]['ref'],
            alt=res.loc[0]['alt']
        )   
        hgnc_flag = False
        if "GN" in res: hgnc=res.loc[0]["GN"]
        if "Symbol" in res: hgnc=res.loc[0]["GN"]
        if hgnc is not None: 
            values["hgnc"] = hgnc
            hgnc_flag = True

        user_flag =check_df(res)
        user_cols = res.columns if user_flag else None

        return render_template('userdb-variant-details.html',
            values=values, hgnc_flag = hgnc_flag,
            df=res, user_cols=user_cols, user_flag=user_flag, zip=zip)

    except Exception as err:
        err_handler(err)
        return render_template('userdb.html',
                column_names=None, 
                column_names_mapper=None, 
                is_none=True, 
                df=None, zip=zip)


def add_data():
    try:
        if request.method == 'POST':
            file = request.files['insert_vcf_file']
            if file.filename == '':
                flash('Lütfen bir dosya seçiniz.')
                return render_template("insert-data.html")
            elif file and allowed_file(file.filename):
                content = file.stream.read() 
                if(content == b''b''):
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                    return render_template("insert-data.html")
                
                file_content = content.decode("utf-8")
                lines = [l for l in io.StringIO(file_content) if not l.startswith('#')]
                input_vcf_df = pd.read_csv(
                    io.StringIO(''.join(lines)),
                    names=["CHROM", "POS", "REF", "ALT", "INFO"], 
                    header=None,
                    dtype={'#CHROM': str, 'POS': int, 'REF': str, 'ALT': str, 'INFO': str},
                    sep='\t'
                ).rename(columns={'#CHROM': 'CHROM'})

                if input_vcf_df is None:  
                    flash('Yüklediğiniz dosyada veri bulunamadı')
                    return render_template("insert-data.html")
                if insert_data(input_vcf_df) == True:            
                    flash('Dosya başarıyla veritabanına eklendi.')
                    return render_template("insert-data.html")
                else: return render_template("insert-data.html")
            else:
                flash('Lütfen VCF uzantılı bir dosya yükleyin.')
                return render_template("insert-data.html")
        else: return render_template("insert-data.html")
    except Exception as err:
        err_handler(err)
        return render_template("insert-data.html")

def dict_page():
    nomenc = excel_to_df(config.DICT_EXCEL_PATH)
    if nomenc is None: isNone = True
    else: isNone = False
    return render_template('dict.html', nomenc=nomenc, isNone=isNone)

def download_data():
    
    path = 'Temp\\results.vcf'
    return send_file(path, as_attachment=True)
