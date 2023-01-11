
from flask import render_template, request, flash

# custom modules

from utils import (
    allowed_file,
    err_handler
)

from db_utils import (
    list_results,
    insert_data
)

from df_utils import(
    excel_to_df,
    read_vcf_from_str
)

import config

# VIEW FUNCTIONS

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
                    return render_template("home.html")
                file_content = content.decode("utf-8")
                input_vcf_df = read_vcf_from_str(file_content)
                if input_vcf_df is None:  
                    flash('Uploaded file is empty.')
                else:
                    res_arr = list_results(input_vcf_df)
                    if res_arr is not None: render_template('results.html', results=res_arr)
            else:
                flash('Only vcf files are allowed')
        
        return render_template('home.html')

    except Exception as err:
        err_handler(err)
        return render_template('home.html')

def view_results(input_vcf_df):
    try:
        print("in view_results")
        res_arr = list_results(input_vcf_df)
        if res_arr is not None: 
            render_template('results_f.html', results=res_arr)
        return render_template('noResults.html')
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
