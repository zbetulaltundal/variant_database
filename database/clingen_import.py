import main
import os
import pandas as pd

def import_clingen_data(conn):
    
    # şuanda bulunulan dizin'i(directory/dir) dönen fonksiyon 
    # cwd = current working directory (şuanda çalışılan dizin)
    cwd = os.getcwd()  # Get the current working directory

    csv_path = f'{cwd}\\data\\ClinGen' # verileri içeren csv dosyasının projede bulunduğu konum
    csv_name = 'Clingen-Gene-Disease-Summary-2022-07-22.csv' # csv dosyasının ismi

    # using pandas read_csv function convert the data to a pandas dataframe
    # pandas(pd) kütüphanesinin read_csv fonksiyonu ile csv dosyası okunur ve data adlı değişkene atanır
    data = pd.read_csv(f'{csv_path}\\{csv_name}') 

    # data değişkeninin her bir satırı iterate edilir
    for row in data.itertuples(): 
        if row[0] > 4:
            gene_symbol = main.check_var(row[1])
            hgnc_id = main.check_var(row[2])
            disease_label = main.check_var(row[3])
            mondo_disease_id = main.check_var(row[4])
            moi = main.check_var(row[5])
            sop = main.check_var(row[6])
            classification = main.check_var(row[7])
            online_report_url = main.check_var(row[8])
            classification_date = main.check_var(row[9])
            gcep = main.check_var((row[10]))
            
            # data formatting
            # veri formatlama
            # convert iso 8601 date format to psql timestamptz format
            # iso 8601 formatındaki tarih bilgisi, postgresql'ın timestamptz formatına dönüştürülür
            if main.check_var(classification_date) != None: 
                # iso 8601 yy-mm-ddThh:mm:ss.mssZ
                # timestamptz yy-mm-dd hh:mm:ss+00 
                date, time = classification_date.split("T", 1)
                f_classification_date = f'{date} {time[:11]}+00'

            # convert HGNC:XXXXX TO XXXXX
            # HGNC:XXXXX formatındaki veri XXXXX formatına dönüştürülür
            if main.check_var(hgnc_id) != None: f_hgnc_id = hgnc_id[5:]
            else: f_hgnc_id = None
            
            # convert MONDO:XXXXXXX TO XXXXXXX
            # MONDO:XXXXX formatındaki veri XXXXX formatına dönüştürülür
            if main.check_var(mondo_disease_id) != None: f_mondo_disease_id = mondo_disease_id[6:]
            else: f_mondo_disease_id = None

            # if no classification information given, set the field to 'None'
            # eğer classification verisi verilmemişse, bu alan 'None'a eşitlenir
            if classification == "No Known Disease Relationship": classification = None

            # insert record into the clingen_variants table
            # bu satırdan alınan bilgiler veritabanına eklenir
            
            # ekleme işlemi için gereken PSQL sorgusu (query)
            query = """INSERT INTO clingen_variants (GENE_SYMBOL, HGNC_ID, DISEASE_LABEL, \
                            MONDO_DISEASE_ID, MOI, SOP, CLASSIFICATION,\
                            ONLINE_REPORT, CLASSIFICATION_DATE, GCEP)\
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            # eklenecek bilgileri içeren liste (record)
            record = (gene_symbol, f_hgnc_id, disease_label, f_mondo_disease_id, \
                        moi, sop, classification, online_report_url, \
                        f_classification_date, gcep)
            
            main.insert_into_db(conn, query, record)
