# dataset_cols = ['Clinical Annotation ID', 'Variant/Haplotypes', 'Gene',
#        'Level of Evidence', 'Level Override', 'Level Modifiers', 'Score_x',
#        'Phenotype Category', 'PMID Count', 'Evidence Count', 'Latest History Date (YYYY-MM-DD)', 'URL',
#        'Specialty Population', 'Genotype/Allele', 'Annotation Text',
#        'Allele Function', 'Evidence ID', 'Evidence Type', 'Evidence URL',
#        'PMID', 'Summary', 'Score_y']


# db_cols = ["Clinical_Annotation_ID", "VARIANT", "GENE", "LEVEL_OF_EVIDENCE", "LEVEL_OVERRIDE",
#              "LEVEL_MODIFIERS", "SCORE", "PHENOTYPE_CATEGORY", "PMID_COUNT", "EVIDENCE_COUNT",
#              "LATEST_HISTORY_DATE", "pharmgkb_URL", "Specialty_Population", "Genotype",
#              "ANNOTATION_TEXT", "Allele_Function", "Evidence_ID", "Evidence_Type", "Evidence_URL", 
#              "Evidence_PMID", "Evidence_Summary", "Evidence_Score"]

# print(len(dataset_cols))
# print(len(db_cols))

# d = dict(zip(dataset_cols, db_cols))

# print(d)

def replace_cols(l):
    l_new = []
    for item in l:
        l_new.append(item.replace(" ", "_"))
    return l_new
    
civic_cols=['GN', 'VT', 'Allele', 'Consequence', 'Entrez_Gene_ID', 
'Feature_type', 'Feature', 'HGVSc', 'HGVSp',
'CIViC_Variant_ID', 'CIViC_Variant_Aliases', 'CIViC_HGVS', 
'Allele_Registry_ID', 'ClinVar_IDs', 'CIViC_Variant_Evidence_Score', 'CIViC_Entity_Type', 'CIViC_Entity_ID', 'CIViC_Entity_URL', 'CIViC_Entity_Source', 'CIViC_Entity_Variant_Origin', 'CIViC_Entity_Status', 'CIViC_Entity_Clinical_Significance', 'CIViC_Entity_Direction', 'CIViC_Entity_Disease', 'CIViC_Entity_Drugs', 'CIViC_Entity_Drug_Interaction_Type', 'CIViC_Evidence_Phenotypes', 'CIViC_Evidence_Level', 'CIViC_Evidence_Rating', 'CIViC_Assertion_ACMG_Codes', 'CIViC_Assertion_AMP_Category', 'CIViC_Assertion_NCCN_Guideline', 'CIVIC_Assertion_Regulatory_Approval', 'CIVIC_Assertion_FDA_Companion_Test']

civic_UI_cols=['HGNC GENE SYMBOL', 'CIViC Variant Name', 'Allele', 
'Consequence', 'Entrez Gene ID', 'CIViC Feature Type', 'CIViC Feature', 
'HGVSc', 'HGVSp','CIViC Variant ID', 'CIViC Variant Aliases', 'CIViC HGVS',
'Allele Registry ID', 'ClinVar IDs', 'CIViC Variant Evidence Score', 
'CIViC Entity Type', 'CIViC Entity ID',  'CIViC Entity URL', 
'CIViC Entity Source', 'CIViC Entity Variant Origin', 'CIViC Entity Status',
'CIViC Entity Clinical Significance', 'CIViC Entity Direction',
'CIViC Entity Disease', 'CIViC Entity Drugs',
'CIViC Entity Drug Interaction Type', 'CIViC Evidence Phenotypes',
'CIViC Evidence Level', 'CIViC Evidence Rating', 'CIViC Assertion ACMG Codes',
 'CIViC Assertion AMP Category', 'CIViC Assertion NCCN Guideline', 
 'CIVIC Assertion Regulatory Approval', 'CIVIC Assertion FDA Companion Test']

print(dict(zip(civic_cols, civic_UI_cols)))