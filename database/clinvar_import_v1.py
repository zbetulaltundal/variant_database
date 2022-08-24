# import scikit-allel
from asyncio.windows_events import NULL
import db_config
import psycopg2 as psql
import sys
import os
import vcf
import main

# CLNDISDB_ABBRV adlı tablo'da verilen disdb_name 'e sahip bir kayıt olup olmadığını gösteren fonksiyon.
# Eğer var ise sonucu liste(tuple) halinde döner
# Eğer yok ise None sonucunu gönderir
def abbrv_exists(conn, disdb_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM  CLNDISDB_ABBRV WHERE NAME = %s", (disdb_name,))
    return cur.fetchone()


def handle_other_infos(conn, info, info_id):
    
    try:
        #'CLNDISDB'
        if main.search_dict(info, 'CLNDISDB') != None:
            for val_str in info['CLNDISDB']:
                if main.check_var(val_str) != None:
                    for sub_str in val_str.split('|'):
                        values = sub_str.split(':')
                        if main.check_var(values) != None:
                            if len(values) == 2:
                                CLNDISDB_NAME, CLNDISDB_ID = values
                                query = """INSERT INTO CLNDISDB (CLNDISDB_NAME, CLNDISDB_ID, INFO_ID)\
                                                VALUES (%s, %s, %s);"""

                                record = (CLNDISDB_NAME, CLNDISDB_ID, info_id)
                                fk = None

                            elif len(values) == 3: 
                                CLNDISDB_NAME, CLNDISDB_NAME_abbrv, CLNDISDB_ID = values
                                check_abbrv = abbrv_exists(conn, CLNDISDB_NAME)
                                if check_abbrv != None:
                                    fk = check_abbrv[0]
                                else:
                                    # insert into CLNDISDB_ABBRV
                                    query = """INSERT INTO CLNDISDB_ABBRV (NAME, ABBRV)\
                                                    VALUES (%s, %s) RETURNING id;"""

                                    record = (CLNDISDB_NAME, CLNDISDB_NAME_abbrv)
                                    fk = main.insert_into_db_returning_id(conn, query, record)
                        
                            query = """INSERT INTO CLNDISDB (CLNDISDB_NAME_ID, CLNDISDB_NAME, CLNDISDB_ID, INFO_ID)\
                                            VALUES (%s, %s, %s, %s);"""

                            record = (fk, CLNDISDB_NAME, CLNDISDB_ID, info_id)

                            
                            main.insert_into_db(conn, query, record)

        #GENEINFO
        if main.search_dict(info, 'GENEINFO') != None:
            for val_str in info['GENEINFO'].split('|'):
                if main.check_var(val_str) == None: continue
                else:
                    values = val_str.split(':')
                    Gene_Sym, Gene_ID = values

                    if main.check_var(Gene_Sym) == None: continue
                    else:
                        query = f'INSERT INTO GENEINFO (Gene_Sym, Gene_ID, INFO_ID)\
                                VALUES (%s, %s, %s);'

                        record = (Gene_Sym, Gene_ID, info_id)

                        main.insert_into_db(conn, query, record)

        #MC   
        if main.search_dict(info, 'MC') != None:
            for val_str in info['MC']:
                if main.check_var(val_str) == None: continue
                else:
                    # Sequence_Ontology_ID|molecular_consequence
                    Seq_Ont_ID, Mol_Conseq = val_str.split('|')
                    query = """INSERT INTO MC (Seq_Ont_ID, Mol_Conseq, INFO_ID)\
                                            VALUES (%s, %s, %s);"""

                    record = (Seq_Ont_ID, Mol_Conseq, info_id)

                    main.insert_into_db(conn, query, record)

        #CLNVI
        if main.search_dict(info, 'CLNVI') != None:
            for val_str in info['CLNVI']:
                if main.check_var(val_str) == None: continue
                else:
                    values = val_str.split(':')
                    if len(values) == 2:
                        SRC, SRC_ID = values
                    else:
                        SRC = values[0]
                        SRC_ID = None

                    query = """INSERT INTO CLNVI (SRC, SRC_ID, INFO_ID)\
                                        VALUES (%s, %s, %s);"""

                    record = (SRC, SRC_ID, info_id)

                    main.insert_into_db(conn, query, record)
        
        DN_FIELDS = ['CLNDN', 'CLNDNINCL']
        for field in DN_FIELDS:
            if main.search_dict(info, field) != None:
                for info_str in info[field]:
                    if main.check_var(info_str) == None: continue
                    else:
                        values = info_str.split('|')
                        if len(values) == 2:
                            DISEASE_NAME, DISEASE_ID = values
                        else:
                            DISEASE_NAME = values[0]
                            DISEASE_ID = None
                        
                        query = f'INSERT INTO {field} (DISEASE_NAME, DISEASE_ID, INFO_ID)\
                        VALUES (%s, %s, %s);'

                        record = (DISEASE_NAME, DISEASE_ID, info_id)

                        main.insert_into_db(conn, query, record)
        
        fields_w_one_dim_list = [("CLNSIG","CLNSIG") , ("CLNSIGCONF","CLNSIGCONF") , ("CLNSIGINCL","CLNSIGINCL"), ("CLNREVSTAT","STAT")]
        for field, col_name in fields_w_one_dim_list:
            if main.search_dict(info, field) != None:
                values = info[field]
                if main.check_var(values) != None:
                    for val in values:
                        query = f'INSERT INTO {field} ({col_name}, INFO_ID)\
                                    VALUES (%s, %s);'

                        record = (val, info_id)

                        main.insert_into_db(conn, query, record)

    except Exception as err:
        print ("Exception has occured:", err)
        print ("Exception type:", type(err))
        err_type, err_obj, traceback = sys.exc_info()
        line_num = traceback.tb_lineno
        # print the connect() error
        print ("\nERROR:", err, "on line number:", line_num)
        print ("traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)

def import_clinvar_data(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    vcf_path = f'{cwd}\data\ClinVar\clinvar.vcf'
    vcf_name = 'clinvar.vcf'
    vcf_reader = vcf.Reader(open(f'{vcf_path}\{vcf_name}'))

    #vcf_cols = vcf_reader._column_headers
    #info_fields = get_info_headers(vcf_reader)
    #print(info_fields)

    for rec in vcf_reader:

        # VARIANTS
        CHROM = main.check_var(rec.CHROM)
        POS = main.check_var(rec.POS)
        ID = main.check_var(rec.ID)
        REF = main.check_var(rec.REF)
        ALT = main.check_var(main.listToString(rec.ALT))
        QUAL = main.check_var(rec.QUAL)
        FILTER = main.check_var(rec.FILTER)

        # INFO
        AF_ESP = main.search_dict(rec.INFO, "AF_ESP")
        AF_EXAC = main.search_dict(rec.INFO, 'AF_EXAC')
        AF_TGP = main.search_dict(rec.INFO, 'AF_TGP')
        ALLELEID = main.search_dict(rec.INFO, 'ALLELEID')
        CLNHGVS = main.search_dict(rec.INFO, 'CLNHGVS')#list
        CLNVC = main.search_dict(rec.INFO, 'CLNVC')
        CLNVCSO = main.search_dict(rec.INFO, 'CLNVCSO')
        DBVARID = main.search_dict(rec.INFO, 'DBVARID')
        ORIGIN = main.search_dict(rec.INFO, 'ORIGIN') #list
        RS = main.search_dict(rec.INFO, 'RS')  #list
        SSR = main.search_dict(rec.INFO, 'SSR')

         # insert record into the INFO table
        query = """INSERT INTO INFO (AF_ESP, AF_EXAC, AF_TGP, \
                        ALLELEID, CLNHGVS, CLNVC, CLNVCSO, DBVARID, \
                           ORIGIN, RS, SSR)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""

        record = (AF_ESP, AF_EXAC, AF_TGP, ALLELEID, \
        CLNHGVS, CLNVC, CLNVCSO, DBVARID, ORIGIN, RS, SSR)
        
        info_id = main.insert_into_db_returning_id(conn, query, record)

        # insert record into the VARIANTS table
        query = """INSERT INTO variant (CHROM, POS, CLINVAR_ID, \
                        REF, ALT, QUAL, FILTER, INFO_ID)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

        record = (CHROM, POS, ID, REF, ALT, QUAL, FILTER, info_id)

        main.insert_into_db(conn, query, record)
        
        handle_other_infos(conn, rec.INFO, info_id)
