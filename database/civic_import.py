import os
import vcf
import common_functions 

def get_csq_fields(vcf_reader):
    fields = []
    csq = vcf_reader.infos['CSQ']
    start_idx = csq.desc.find("Format: ") + 8

    for f in csq.desc[start_idx: ].split("|"):
        fields.append(f)

    return fields

def import_civic_data(conn):
    
    # open the csv data
    cwd = os.getcwd()  # Get the current working directory
    vcf_path = f'{cwd}\\data'
    vcf_name = 'nightly-civic_accepted_and_submitted.vcf'
    vcf_reader = vcf.Reader(open(f'{vcf_path}\\{vcf_name}'))

    csq_fields = get_csq_fields(vcf_reader)
    print(csq_fields)

    for rec in vcf_reader:
        dict = {}
        dict['CHROM'] = common_functions.check_var(rec.CHROM)
        dict['POS'] = str(common_functions.check_var(rec.POS))
        dict['VAR_ID'] = common_functions.check_var(rec.ID)
        dict['REF'] = common_functions.check_var(rec.REF)
        dict['ALT'] = common_functions.check_var(common_functions.listToString(rec.ALT))
        dict['QUAL'] = common_functions.check_var(rec.QUAL)
        dict['FILTER'] = common_functions.check_var(rec.FILTER)

        for key, val in rec.INFO.items():
            if key =="CSQ":
                for csq_val, csq_key in zip(val[0].split("|"), csq_fields):
                    t_csq_val = common_functions.check_var(csq_val)
                    dict["INFO."+csq_key] = t_csq_val
            else:
                dict["INFO."+key] = common_functions.check_var(val)

       # insert record into the CIVic_variants table
        query = """INSERT INTO civic_variants ( CHROM ,  POS ,  VAR_ID ,  REF ,  ALT ,  QUAL ,  FILTER ,\
                     GN ,  VT ,  Allele ,  Consequence ,  SYMBOL ,  Entrez_Gene_ID ,  Feature_type ,  Feature ,  HGVSc , \
                     HGVSp ,  CIViC_Var_Name ,  CIViC_Var_ID ,  CIViC_Var_Aliases ,  CIViC_HGVS , \
                     Allele_Registry_ID ,  ClinVar_ID ,  CIViC_Var_Ev_Score ,  CIViC_Ent_Type , \
                     CIViC_Ent_ID ,  CIViC_Ent_URL ,  CIViC_Ent_Src ,  CIViC_Ent_Var_Origin ,\
                     CIViC_Ent_Stat ,  CIViC_Clin_Sig ,  CIViC_Ent_Dir , \
                     CIViC_Ent_Disease ,  CIViC_Ent_Drugs ,  CIViC_Ent_Drug_Int , \
                     CIViC_Ev_Phenotypes ,  CIViC_Ev_Level ,  CIViC_Ev_Rating , \
                     CIViC_Assertion_ACMG_Codes ,  CIViC_Assertion_AMP_Cat ,\
                     CIViC_Assertion_NCCN_Guid ,  CIViC_Assertion_Regu_Appr_Guid ,\
                     CIViC_Assertion_FDA_Comp_Test_Guid) """

        format_spec =f'VALUES ({42*"%s,"}%s);'
        tupl = tuple(dict.values())

        # 89th line gives an exception
        if len(tupl) == 33: 
            print(tupl)
            continue
        

        common_functions.insert_into_db(conn, f'{query}{format_spec}', tupl)
