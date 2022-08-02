CREATE DATABASE "clingen"
  WITH OWNER "postgres"
  ENCODING 'UTF8';

CREATE TABLE clingen_variants (
    ID  SERIAL PRIMARY KEY, 
    GENE_SYMBOL  VARCHAR(20), -- hgnc gene symbol
    HGNC_ID  VARCHAR(5), -- HGNC gen id
    DISEASE_LABEL TEXT,
    MONDO_DISEASE_ID VARCHAR(7),
    MOI VARCHAR(20),
    SOP VARCHAR(4),
    CLASSIFICATION VARCHAR(20),
    ONLINE_REPORT TEXT,
    CLASSIFICATION_DATE TIMESTAMPTZ,
    GCEP TEXT
);

select * from clingen_variants;


CREATE DATABASE "CIVic"
  WITH OWNER "postgres"
  ENCODING 'UTF8';

CREATE TABLE CIVic_variants (
    ID  SERIAL PRIMARY KEY, 
    CHROM  VARCHAR(20),
    POS  VARCHAR(5),
    VAR_ID VARCHAR(10), -- The identifier of the variation, ??? same as hgnc_id??
    REF VARCHAR(7),
    ALT VARCHAR(50), --Alternation
    QUAL VARCHAR(20), -- ??
    FILTER VARCHAR(20),
    -- info
    GN VARCHAR(8), -- hgnc gene symbol
    VT TEXT, -- CIViC Variant Name
    -- info.csq
    Allele VARCHAR(50), -- verilerde
    Consequence VARCHAR(50), -- missensed variant, Splice_Donor variant
    SYMBOL VARCHAR(8),  -- hgnc gene symbol
    Entrez_Gene_ID VARCHAR(10), -- ?
    Feature_type VARCHAR(30), 
    Feature VARCHAR(20),  --ENST00000415913
    HGVSc VARCHAR(40), --
    HGVSp VARCHAR(40), 
    CIVic_Var_Name TEXT, --CIViC Variant Name
    CIVic_Var_ID VARCHAR(10),  -- The identifier of the variation,
    ---- BURADA KALDIK --- 
    CIVic_Var_Aliases VARCHAR(50), 
    CIVic_HGVS VARCHAR(20), 
    Allele_Registry_ID VARCHAR(20), 
    ClinVar_ID VARCHAR(20), 
    CIViC_Var_Ev_Score VARCHAR(20), --CIViC Variant Evidence Score
    CIViC_Ent_Type VARCHAR(20), --CIViC Entity Type
    CIViC_Ent_ID VARCHAR(20), --CIViC Entity ID
    CIViC_Ent_URL VARCHAR(20), --CIViC Entity URL
    CIViC_Ent_Src VARCHAR(20), --CIViC Entity Source
    CIViC_Ent_Var_Origin VARCHAR(20), -- CIViC Entity Variant Origin
    CIViC_Ent_Stat VARCHAR(20), --CIViC Entity Status
    CIViC_Clin_Sig VARCHAR(20), --CIViC Entity Clinical Significance
    CIViC_Ent_Dir VARCHAR(20), --CIViC Entity Direction
    CIViC_Ent_Disease VARCHAR(20), --CIViC Entity Disease
    CIViC_Ent_Drugs VARCHAR(20), --CIViC Entity Drugs
    CIViC_Ent_Drug_Interaction VARCHAR(20), --CIViC Entity Drug Interaction Type
    CIViC_Ev_Phenotypes VARCHAR(20), --CIViC Evidence Phenotypes
    CIViC_Ev_Level VARCHAR(20), --CIViC Evidence Level
    CIViC_Ev_Rating VARCHAR(20), --CIViC Evidence Rating
    CIViC_Assertion_ACMG_Codes VARCHAR(20), --CIViC Assertion ACMG Codes
    CIViC_Assertion_AMP_Cat VARCHAR(20), --CIViC Assertion AMP Category
    CIViC_Assertion_NCCN Guideline VARCHAR(20), --CIViC Assertion AMP Category
    CIViC_Assertion_Regu_Appr Guideline VARCHAR(20), --CIVIC Assertion Regulatory Approval
    CIViC_Assertion_FDA_Comp_Test Guideline VARCHAR(20) --CIVIC Assertion FDA Companion Test 
);
