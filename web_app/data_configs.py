
pharmgkb_mapper = {
    "gene":"HGNC Gene Symbol",
    "Clinical_Annotation_ID":"Clinical Annotation ID", 
    "level_of_evidence": "Evidence Level", 
    "LEVEL_OVERRIDE": "Level Override", 
    "LEVEL_MODIFIERS": "Level Modifiers", 
    "SCORE": "SCORE",
    "PHENOTYPE_CATEGORY":"Phenotype Category",
    "PMID_COUNT":"PMID Count",
    "EVIDENCE_COUNT":"Evidence COUNT",
    "LATEST_HISTORY_DATE":"Latest History Date",
    "pharmgkb_URL":"Pharmgkb URL",
    "Specialty_Population":"Specialty Population",
    "Genotype":"Genotype",
    "ANNOTATION_TEXT":"Annotation Text",
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
    'allele': 'Allele', 
    'consequence': 'Consequence',
    'entrez_gene_id': 'Entrez Gene ID', 
    'feature_type': 'CIViC Feature Type', 
    'feature': 'CIViC Feature', 
    'hgvsc': 'HGVSc', 
    'hgvsp': 'HGVSp', 
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

civic_col_name_mapper2 = {
    'gn': 'HGNC Gene Symbol', 
    'symbol': 'HGNC Gene Symbol', 
    "vt" : "CIViC Variant Name",
    'civic_variant_name': 'CIViC Variant Name', 
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