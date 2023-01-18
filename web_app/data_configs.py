
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


id_cols =  ['CHROM', 'POS', 'REF', 'ALT']


pharmgkb_mapper = {
    "gene":"HGNC Gene Symbol",
    "Clinical_Annotation_ID":"Clinical Annotation ID", 
    "level_of_evidence": "Evidence Level", 
    "LEVEL_OVERRIDE": "LEVEL OVERRIDE", 
    "LEVEL_MODIFIERS": "LEVEL MODIFIERS", 
    "SCORE": "SCORE",
    "PHENOTYPE_CATEGORY":"PHENOTYPE CATEGORY",
    "PMID_COUNT":"PMID COUNT",
    "EVIDENCE_COUNT":"EVIDENCE COUNT",
    "LATEST_HISTORY_DATE":"LATEST HISTORY DATE",
    "pharmgkb_URL":"pharmgkb URL",
    "Specialty_Population":"Specialty Population",
    "Genotype":"Genotype",
    "ANNOTATION_TEXT":"ANNOTATION TEXT",
    "Allele_Function":"Allele Function",
    "Evidence_ID":"Evidence ID",
    "Evidence_Type":"Evidence Type",
    "Evidence_URL":"Evidence URL",
    "Evidence_PMID":"Evidence PMID",
    "Evidence_Summary":"Evidence Summary",
    "Evidence_Score":"Evidence Score",
    "id":"variant_id"
    }

'''
pharmgkb drug names
pharmgkb haplotypes
pharmgkb phenotypes
'''

civic_col_name_mapper = {
    'gn': 'HGNC Gene Symbol', 
    'vt': 'CIViC Variant Name', 
    'allele': 'Allele', 
    'consequence': 'Consequence', 
    'symbol': 'Symbol', 
    'entrez_gene_id': 'Entrez Gene ID', 
    'feature_type': 'CIViC Feature Type', 
    'feature': 'CIViC Feature', 
    'hgvsc': 'HGVSc', 
    'hgvsp': 'HGVSp', 
    'civic_variant_name': 'CIViC Variant Name', 
    'civic_variant_id': 'CIViC Variant ID', 
    'civic_variant_aliases': 'CIViC Variant Aliases',
     'civic_hgvs': 'CIViC HGVS', 
     'allele_registry_id': 'Allele Registry ID', 
     'clinvar_ids': 'ClinVar IDs',
     'civic_variant_evidence_score': 'CIViC Variant Evidence Score', 
     'civic_entity_type': 'CIViC Entity Type', 
     'civic_entity_id': 'CIViC Entity ID', 
    'civic_entity_url': 'CIViC Entity URL', 
    'civic_entity_source': 'CIViC Entity Source', 
    'civic_entity_variant_origin': 'CIViC Entity Variant Origin', 
    'civic_entity_status': 'CIViC Entity Status', 
    'civic_entity_clinical_significance': 'CIViC Entity Clinical Significance', 
    'civic_entity_direction': 'CIViC Entity Direction', 
    'civic_entity_disease': 'CIViC Entity Disease', 
    'civic_entity_drugs': 'CIViC Entity Drugs', 
    'civic_entity_drug_interaction_type': 'CIViC Entity Drug Interaction Type', 
    'civic_evidence_phenotypes': 'CIViC Evidence Phenotypes', 
    'civic_evidence_level': 'CIViC Evidence Level', 
    'civic_evidence_rating': 'CIViC Evidence Rating', 
    'civic_assertion_acmg_codes': 'CIViC Assertion ACMG Codes', 
    'civic_assertion_amp_category': 'CIViC Assertion AMP Category', 
    'civic_assertion_nccn_guideline': 'CIViC Assertion NCCN Guideline',
     'civic_assertion_regulatory_approval': 'CIVIC Assertion Regulatory Approval', 
     'civic_assertion_fda_companion_test': 'CIVIC Assertion FDA Companion Test', 
     'var_id': 'dbSNP RefSNP ID',
     }

#other_cols = ["CHROM", "POS", "REF", "ALT", "QUAL"]

clingen_col_name_mapper = {
    "gene_symbol":"HGNC Gene Symbol", 
    "HGNC_ID": "HGNC Gene ID", 
    "disease_label": "Disease Label",
    "MONDO_DISEASE_ID": "MONDO Disease ID",
    "MOI": "Mode of Inheritance",
    "SOP": "SOP",
    "CLASSIFICATION":"ClinGen Classification", 
    "online_report":"ClinGen URL", 
    "classification_date":"ClinGen Classification Date",
    "GCEP" :"GCEP"
    }


uniprot_col_mapper = {
    "id":"variant_id",
    "gene_name":"HGNC Gene Symbol",
    "AC" : "UniProtKB Accession",
    "variant_aa_change" : "Variant AA Change",
    "source_db_id" : "dbSNP identifier",
    "consequence_type" : "UniProt Consequence Type",   
    "clinical_significance" : "Clinical Significance",
    "phenotype_disease" : "Phenotype disease", 
    "phenotype_disease_source" : "Phenotype Disease Source",
    "cytogenetic_band" : "Cytogenetic Band",
    "chromosome_coordinate" : "Chromosome Coordinate",
    "ensembl_gene_ID" : "Ensembl Gene ID",
    "ensembl_transcript_ID" : "Ensembl Transcript ID",
    "ensembl_translation_ID" : "Ensembl Translation ID"
}

# Uniprot Evidence Names

# USER DB HAS ONLY FOLLOWING
other_cols = ["CHROM", "POS", "VAR_ID", "REF", "ALT", "QUAL"]


clinvar_mapper={
    "id":"info_id",
    "alleleid": "ClinVar Allele ID",
    "clnhgvs": "ClinVar HGVS",
    "clnvc" : "ClinVar Variant Type",
    "clnvcso" : "ClinVar SO",
    "origin" : "ClinVar Origin",
    "af_esp" : "AF ESP",
    "af_exac" : "AF EXAC",
    "af_tgp" : "AF TGP",
    "dbvarid" : "dbVar id",
    "rs" : "dbSNP id",
    "ssr" : "SSR",
    "clinvar_id":"ClinVar Variation ID",
    # "CLNREVSTAT":"ClinVar Review Status",
    }

# ["CHROM", "POS", "CLINVAR_ID", "REF", "ALT", "QUAL"]
# clndisdb
#     FILTER TEXT,
#     INFO_ID INT,
# gene info 
# clnvi
# mc
# clnsig
# clnsigconf
# clnsigincl
# review status