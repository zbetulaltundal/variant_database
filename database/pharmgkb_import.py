
import os

from utils import(
    err_handler,
    check_value,
    join_data_frames,
    tsv_to_df
)

from db_utils import(
    insert_into_db_returning_id_V2,
    insert_csv
)

join_cols = ['Clinical Annotation ID']

dataset_to_db_col_mapper = {'Clinical Annotation ID': 'Clinical_Annotation_ID', 'Variant/Haplotypes': 'VARIANT', 'Gene': 'GENE', 'Level of Evidence': 'LEVEL_OF_EVIDENCE', 'Level Override': 'LEVEL_OVERRIDE', 'Level Modifiers': 'LEVEL_MODIFIERS', 'Score_x': 'SCORE', 'Phenotype Category': 'PHENOTYPE_CATEGORY', 'PMID Count': 'PMID_COUNT', 'Evidence Count': 'EVIDENCE_COUNT', 'Latest History Date (YYYY-MM-DD)': 'LATEST_HISTORY_DATE', 'URL': 'pharmgkb_URL', 'Specialty Population': 'Specialty_Population', 'Genotype/Allele': 'Genotype', 'Annotation Text': 'ANNOTATION_TEXT', 'Allele Function': 'Allele_Function', 'Evidence ID': 'Evidence_ID', 'Evidence Type': 
'Evidence_Type', 'Evidence URL': 'Evidence_URL', 'PMID': 'Evidence_PMID', 'Summary': 'Evidence_Summary', 'Score_y': 'Evidence_Score'}

def split_drugs_and_phenotypes(str_val):

    l_str_val = str_val.split(";")[:-1]
    if(len(l_str_val) == 0): return f"('{str_val}')"

    res_str = ""
    for elem in l_str_val:
        res_str = f"{res_str},('{elem}')"

    return res_str[1:]


def insert_drug_data(drug_list_str, conn):
    try:
        if check_value(drug_list_str): 
            drug_records = split_drugs_and_phenotypes(drug_list_str)
            query = f"""INSERT INTO DRUG (DRUG) VALUES {drug_records} RETURNING id;"""
            return str(insert_into_db_returning_id_V2(conn, query))
        else: return None
        
    except Exception as err:
        err_handler(err)
        return None


def insert_phenotype_data(phenotype_list_str, conn):
    try:
        if check_value(phenotype_list_str):
            p_records = split_drugs_and_phenotypes(phenotype_list_str)
            query = f"""INSERT INTO PHENOTYPE (PHENOTYPE_NAME) VALUES {p_records} RETURNING id;"""
            p_id = str(insert_into_db_returning_id_V2(conn, query))
            return p_id
        else: return None
        
    except Exception as err:
        err_handler(err)
        return None

def set_to_not_scored(score_y):
    try:
        if check_value(score_y):
            if score_y == 'This annotation is not used for clinical annotation scoring.':
                return 'NS'
            else: return score_y
        else: return None
    except Exception as err:
        err_handler(err)
   
def insert_df(conn, df):
    
    try:
        #add 'drug_id' column to end of DataFrame and insert drug values to database
        df['DRUG_ID'] = df['Drug(s)'].apply(lambda x: insert_drug_data(x, conn))

        #add 'phenotype_id' column to end of DataFrame and insert phenotype values to database
        df['PHENOTYPE_ID'] = df['Phenotype(s)'].apply(lambda x: insert_phenotype_data(x, conn))

        # rename not scored records as 'NS'
        if 'Score_y' in df.columns:
            df['Score_y'] = df['Score_y'].apply(set_to_not_scored)
        
        # drop unnecessary columns
        df.drop(columns=['Drug(s)', 'Phenotype(s)'], inplace=True)

        df.rename(columns = dataset_to_db_col_mapper, inplace = True)

        df.to_csv("temp\\pharmgkb_tbl.csv")

        insert_csv(conn, "temp\\pharmgkb_tbl.csv", "pharmgkb")

    except Exception as err:
        err_handler(err)

def import_pharmgkb(conn):
    
    try:
        # open the csv
        cwd = os.getcwd()  # Get the current working directory
        folder_path = f'{cwd}\\data\\clinicalAnnotations\\'
        filenames = ["clinical_annotations.tsv", "clinical_ann_alleles.tsv", "clinical_ann_evidence.tsv"]
        data_frames = []
        for filename in filenames:
            df = tsv_to_df(folder_path, filename)
            data_frames.append(df)
        
        df_merged = join_data_frames(data_frames, join_cols)

        insert_df(conn, df_merged)

    except Exception as err:
        err_handler(err)
