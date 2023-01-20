
# civic_col_name_mapper = {
#     'GN': 'HGNC GENE SYMBOL', 
#     'VT': 'CIViC Variant Name', 
#     'Allele': 'Allele', 'Consequence': 'Consequence', 'Entrez_Gene_ID': 'Entrez Gene ID', 'Feature_type': 'CIViC Feature Type', 
#     'Feature': 'CIViC Feature', 'HGVSc': 'HGVSc', 'HGVSp': 'HGVSp', 
#     'CIViC_Variant_ID': 'CIViC Variant ID', 
#     'CIViC_Variant_Aliases': 'CIViC Variant Aliases', 'CIViC_HGVS': 'CIViC HGVS', 
#     'Allele_Registry_ID': 'Allele Registry ID', 'ClinVar_IDs': 'ClinVar IDs', 'CIViC_Variant_Evidence_Score': 'CIViC Variant Evidence Score', 
#     'CIViC_Entity_Type': 'CIViC Entity Type', 'CIViC_Entity_ID': 'CIViC Entity ID', 'CIViC_Entity_URL': 'CIViC Entity URL', 'CIViC_Entity_Source': 'CIViC Entity Source', 
#     'CIViC_Entity_Variant_Origin': 'CIViC Entity Variant Origin', 'CIViC_Entity_Status': 'CIViC Entity Status', 
#     'CIViC_Entity_Clinical_Significance': 'CIViC Entity Clinical Significance', 
#     'CIViC_Entity_Direction': 'CIViC Entity Direction', 'CIViC_Entity_Disease': 'CIViC Entity Disease', 
#     'CIViC_Entity_Drugs': 'CIViC Entity Drugs', 'CIViC_Entity_Drug_Interaction_Type': 'CIViC Entity Drug Interaction Type', 'CIViC_Evidence_Phenotypes': 'CIViC Evidence Phenotypes', 
#     'CIViC_Evidence_Level': 'CIViC Evidence Level', 'CIViC_Evidence_Rating': 'CIViC Evidence Rating', 'CIViC_Assertion_ACMG_Codes': 'CIViC Assertion ACMG Codes', 
#     'CIViC_Assertion_AMP_Category': 'CIViC Assertion AMP Category', 'CIViC_Assertion_NCCN_Guideline': 'CIViC Assertion NCCN Guideline', 'CIVIC_Assertion_Regulatory_Approval': 'CIVIC Assertion Regulatory Approval', 
#     'CIVIC_Assertion_FDA_Companion_Test': 'CIVIC Assertion FDA Companion Test',
#     "VAR_ID":"dbSNP RefSNP ID"}

# d_new = dict()
# for val in civic_col_name_mapper:
#     d_new[val.lower()]  = civic_col_name_mapper[val]

# print(d_new)
import pandas as pd
d = {
    'Name':['Ram','Shyam','Seeta','Geeta'],
    'Age':[20,21,20,21]
}

# Creating a DataFrame
df = pd.DataFrame(d)

# Display original DataFrame
print("Original DataFrame:\n",df,"\n")

print(df.loc[0].to_dict())