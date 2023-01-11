
clingen_cols = ['GENE_SYMBOL', 'HGNC_ID', 'DISEASE_LABEL', 'MONDO_DISEASE_ID', 
    'MOI', 'SOP', 'CLASSIFICATION', 'ONLINE_REPORT', 'CLASSIFICATION_DATE', 'GCEP']

# exclude CIViC_Var_Name,GN
civic_cols = ['CHROM' ,  'POS' ,  'VAR_ID' ,  'REF' ,  'ALT' , 'QUAL', 'FILTER', 'GN', 'VT', 'Allele', 'Consequence', 'SYMBOL', 
        'Entrez_Gene_ID', 'Feature_type', 'Feature', 'HGVSc', 'HGVSp', 'CIViC_Var_Name', 'CIViC_Var_ID', 'CIViC_Var_Aliases', 
        'CIViC_HGVS', 'Allele_Registry_ID', 'ClinVar_ID', 'CIViC_Var_Ev_Score', 'CIViC_Ent_Type', 
        'CIViC_Ent_ID', 'CIViC_Ent_URL', 'CIViC_Ent_Src', 'CIViC_Ent_Var_Origin', 'CIViC_Ent_Stat',
        'CIViC_Clin_Sig', 'CIViC_Ent_Dir', 'CIViC_Ent_Disease', 'CIViC_Ent_Drugs', 'CIViC_Ent_Drug_Int', 
        'CIViC_Ev_Phenotypes', 'CIViC_Ev_Level', 'CIViC_Ev_Rating', 'CIViC_Assertion_ACMG_Codes',
        'CIViC_Assertion_AMP_Cat', 'CIViC_Assertion_NCCN_Guid', 'CIViC_Assertion_Regu_Appr_Guid', 
        'CIViC_Assertion_FDA_Comp_Test_Guid']

pharmgkb_cols = ["Clinical_Annotation_ID", "VARIANT", "GENE", "LEVEL_OF_EVIDENCE", "LEVEL_OVERRIDE",
             "LEVEL_MODIFIERS", "SCORE", "PHENOTYPE_CATEGORY", "PMID_COUNT", "EVIDENCE_COUNT",
             "LATEST_HISTORY_DATE", "pharmgkb_URL", "Specialty_Population", "Genotype",
             "ANNOTATION_TEXT", "Allele_Function", "Evidence_ID", "Evidence_Type", "Evidence_URL", 
             "Evidence_PMID", "Evidence_Summary", "Evidence_Score"]


pharmgkb_col_name_mapper = {"GENE":"HGNC GENE SYMBOL", "LEVEL_OF_EVIDENCE": "EVIDENCE LEVEL"}

civic_col_name_mapper = {
    'GN': 'HGNC GENE SYMBOL', 
    'VT': 'CIViC Variant Name', 
    'Allele': 'Allele', 'Consequence': 'Consequence', 'Entrez_Gene_ID': 'Entrez Gene ID', 'Feature_type': 'CIViC Feature Type', 
    'Feature': 'CIViC Feature', 'HGVSc': 'HGVSc', 'HGVSp': 'HGVSp', 
    'CIViC_Variant_ID': 'CIViC Variant ID', 
    'CIViC_Variant_Aliases': 'CIViC Variant Aliases', 'CIViC_HGVS': 'CIViC HGVS', 
    'Allele_Registry_ID': 'Allele Registry ID', 'ClinVar_IDs': 'ClinVar IDs', 'CIViC_Variant_Evidence_Score': 'CIViC Variant Evidence Score', 
    'CIViC_Entity_Type': 'CIViC Entity Type', 'CIViC_Entity_ID': 'CIViC Entity ID', 'CIViC_Entity_URL': 'CIViC Entity URL', 'CIViC_Entity_Source': 'CIViC Entity Source', 
    'CIViC_Entity_Variant_Origin': 'CIViC Entity Variant Origin', 'CIViC_Entity_Status': 'CIViC Entity Status', 
    'CIViC_Entity_Clinical_Significance': 'CIViC Entity Clinical Significance', 
    'CIViC_Entity_Direction': 'CIViC Entity Direction', 'CIViC_Entity_Disease': 'CIViC Entity Disease', 
    'CIViC_Entity_Drugs': 'CIViC Entity Drugs', 'CIViC_Entity_Drug_Interaction_Type': 'CIViC Entity Drug Interaction Type', 'CIViC_Evidence_Phenotypes': 'CIViC Evidence Phenotypes', 
    'CIViC_Evidence_Level': 'CIViC Evidence Level', 'CIViC_Evidence_Rating': 'CIViC Evidence Rating', 'CIViC_Assertion_ACMG_Codes': 'CIViC Assertion ACMG Codes', 
    'CIViC_Assertion_AMP_Category': 'CIViC Assertion AMP Category', 'CIViC_Assertion_NCCN_Guideline': 'CIViC Assertion NCCN Guideline', 'CIVIC_Assertion_Regulatory_Approval': 'CIVIC Assertion Regulatory Approval', 
    'CIVIC_Assertion_FDA_Companion_Test': 'CIVIC Assertion FDA Companion Test'}

clingen_col_name_mapper = {"gene_symbol":"HGNC GENE SYMBOL", "gene_id": "HGNC GENE ID", "disease_label": "DISEASE LABEL",
                        "CLASSIFICATION":"CLINGEN CLASSIFICATION", "disease_id":"MONDO disease id",
                        "online_report":"CLINGEN URL", "classification_date":"CLINGEN CLASSIFICATION DATE"}

id_cols =  ['CHROM', 'POS', 'REF', 'ALT']


clinvar_info_col_name_mapper={
    "ALLELEID": "ClinVar Allele ID",
    "CLNHGVS": "ClinVar HGVS",
    "CLNVC" : "ClinVar VC",
    "CLNVCSO" : "ClinVar SO",
    "ORIGIN" : "ClinVar Origin",
    "AF_ESP" : "AF ESP",
    "AF_EXAC" : "AF EXAC",
    "AF_TGP" : "AF TGP",
    "DBVARID" : "dbVar id",
    "RS" : "dbSNP id",
    "SSR" : "SSR"
    }

uniprot_variant_col_mapper = {
    "gene_name":"HGNC GENE SYMBOL"
}