
from flask import render_template, request, flash, send_file
import timeit 

# custom modules

from db_utils import(
    
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
    join_data_frames,
    write_csv
)

import config

# VIEW FUNCTIONS

def variant_details(chrom, pos, alt, ref, hgnc=None):
    try:
        # tüm özellikleri listele, bir kısmını topluca yukarda, 
        # bazılarını dblere göre kategorize edip aşağıda 
        df_joined, civic_df, clinvar_df, pharmgkb_df, clingen_df = fetch_variant_data(chrom, pos, ref, alt, hgnc)
        cols = df_joined.columns
        mapper = dict()
        for col in cols:
            mapper[col] = col.replace(" ", "-")   

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

        civic_cols = civic_df.columns if civic_flag else None
        clinvar_cols = clinvar_df.columns if clinvar_flag else None
        clingen_cols = clingen_df.columns if clingen_flag else None
        pharmgkb_cols = pharmgkb_df.columns if pharmgkb_flag else None
        clinvar_cols = clinvar_df.columns if clinvar_flag else None

        return render_template('variant-details.html',
            values=values,
            civic=civic_df, 
            civic_cols=civic_cols,
            clinvar_cols=clinvar_cols,
            clingen_cols=clingen_cols,
            pharmgkb_cols=pharmgkb_cols,
            clingen=clingen_df, 
            clinvar=clinvar_df, 
            pharmgkb=pharmgkb_df, 
            clingen_flag=clingen_flag,
            civic_flag=civic_flag,
            clinvar_flag=clinvar_flag,
            pharmgkb_flag=pharmgkb_flag,
            df=df_joined, zip=zip)

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

def upload_vcf_file():
    is_none = True

    try:
        if request.method == 'POST':
            file = request.files['vcf_file']
            if file.filename == '':
                flash('Please select a file')
            elif file and allowed_file(file.filename):
                content = file.read() 
                if(content == b''b''): 
                    flash('Yüklediğiniz dosyada veri bulunamadı.')
                    return render_template("home.html")
                file_content = content.decode("utf-8")
                input_vcf_df = read_vcf_from_str(file_content)
                if input_vcf_df is None:  
                    flash('Uploaded file is empty.')
                else:
                    t_0 = timeit.default_timer()
                    res_df = list_results(input_vcf_df)
                    is_none = not check_df(res_df)
                    if is_none == False:        
                        path = 'Temp\\results.csv'
                        write_csv(res_df, path)
                        cols = res_df.columns
                        mapper = dict()
                        for col in cols:
                            mapper[col] = col.replace(" ", "-")
                        
                        return render_template('results.html',
                                column_names=cols, 
                                column_names_mapper=mapper, 
                                is_none=is_none, 
                                res_df=res_df, zip=zip)

                    t_1 = timeit.default_timer()
                    
                    elapsed_time = round((t_1 - t_0) * 10 ** 9, 3)

                    print(f"results fetched in {elapsed_time} ms")
            else:
                flash('Only vcf files are allowed')
        
        return render_template('results.html', res_df=None, column_names=None, is_none=True)

    except Exception as err:
        err_handler(err)
        return render_template('results.html', res_df=None, column_names=None, is_none=True)

def home_page():
    print("in home_page")
    return render_template("home.html")

def add_data_page():
    print("in add_data page")
    return render_template("veri-ekle.html")

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
                if insert_data(input_vcf_df) == True:            
                    flash('Dosya başarıyla veritabanına eklendi.')
                    return render_template("veri-ekle.html")
                else: return render_template("veri-ekle.html")
            else:
                flash('Lütfen VCF uzantılı bir dosya yükleyin.')
                return render_template("veri-ekle.html")
        else: return render_template("veri-ekle.html")
    except Exception as err:
        err_handler(err)
        return render_template("veri-ekle.html")

def dict_page():
    nomenc = excel_to_df(config.DICT_EXCEL_PATH)
    if nomenc is None: isNone = True
    else: isNone = False
    return render_template('dict.html', nomenc=nomenc, isNone=isNone)

def download_data():
    
    path = 'Temp\\results.csv'
    return send_file(path, as_attachment=True)
