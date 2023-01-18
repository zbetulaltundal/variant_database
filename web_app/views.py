
from flask import render_template, request, flash, send_file
import timeit 

# custom modules

from db_utils import (
    list_results,
    insert_data
)

from utils import(
    allowed_file,
    err_handler,
    excel_to_df,
    read_vcf_from_str
)

import config

# VIEW FUNCTIONS

def upload_vcf_file():
    try:
        isNone = True
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
                    isNone = res_df is None
                    if isNone == False: 
                        res_df.to_csv("Temp\\results.csv")
                        print(res_df)
                        return render_template('results.html',
                                column_names=res_df.columns, 
                                isNone=isNone, 
                                res_df=res_df, zip=zip)

                    t_1 = timeit.default_timer()
                    
                    elapsed_time = round((t_1 - t_0) * 10 ** 9, 3)

                    print(f"results fetched in {elapsed_time} ms")
            else:
                flash('Only vcf files are allowed')
        
        return render_template('results.html', isNone=isNone)

    except Exception as err:
        err_handler(err)
        return render_template('results.html', isNone=isNone)

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
