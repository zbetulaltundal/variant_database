CREATE TABLE INFO (
    ID  SERIAL PRIMARY KEY, 
    GN TEXT,
    VT TEXT,
    Allele TEXT,
    Consequence TEXT,
    SYMBOL TEXT,
    Entrez_Gene_ID TEXT,
    Feature_type TEXT,
    Feature TEXT,
    HGVSc TEXT,
    HGVSp TEXT,
    CIViC_Variant_Name TEXT,
    CIViC_Variant_ID TEXT,
    CIViC_Variant_Aliases TEXT,
    CIViC_HGVS TEXT,
    Allele_Registry_ID TEXT,
    ClinVar_IDs TEXT,
    CIViC_Variant_Evidence_Score TEXT,
    CIViC_Entity_Type TEXT,
    CIViC_Entity_ID TEXT,
    CIViC_Entity_URL TEXT,
    CIViC_Entity_Source TEXT,
    CIViC_Entity_Variant_Origin TEXT,
    CIViC_Entity_Status TEXT,
    CIViC_Entity_Clinical_Significance TEXT,
    CIViC_Entity_Direction TEXT,
    CIViC_Entity_Disease TEXT,
    CIViC_Entity_Drugs TEXT,
    CIViC_Entity_Drug_Interaction_Type TEXT,
    CIViC_Evidence_Phenotypes TEXT,
    CIViC_Evidence_Level TEXT,
    CIViC_Evidence_Rating TEXT,
    CIViC_Assertion_ACMG_Codes TEXT,
    CIViC_Assertion_AMP_Category TEXT,
    CIViC_Assertion_NCCN_Guideline TEXT,
    CIVIC_Assertion_Regulatory_Approval TEXT,
    CIVIC_Assertion_FDA_Companion_Test TEXT
);


CREATE TABLE variant (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,--an identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    VAR_ID TEXT, -- The identifier of the variation, ??? same as DBSNPİD??
    REF TEXT,
    ALT TEXT, --Alternation
    QUAL TEXT, -- 
    FILTER TEXT,
    INFO_ID INT,
    CONSTRAINT fk_INFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);


-- CREATE TABLE INFO (
--     GN TEXT, -- hgnc gene symbol -- info
--     VT TEXT, -- CIViC Variant Name
--     Allele TEXT, -- verilerde -- info.csq
--     Consequence TEXT, -- missensed variant, Splice_Donor variant
--     SYMBOL TEXT,  -- hgnc gene symbol
--     Entrez_Gene_ID TEXT, -- ?
--     Feature_type TEXT, 
--     Feature TEXT,  --ENST00000415913
--     HGVSc TEXT, --
--     HGVSp TEXT, 
--     CIVic_Var_Name TEXT, --CIViC Variant Name
--     CIVic_Var_ID TEXT,  -- The identifier of the variation,
--     CIVic_Var_Aliases TEXT, -- Alternate names of a variant 
--     CIVic_HGVS TEXT, -- NP, NM, NC ??
--     Allele_Registry_ID TEXT, --The ClinGen Allele Registry ID associated with this variant.
--     ClinVar_ID TEXT, 
--     CIViC_Var_Ev_Score TEXT, --CIViC Variant Evidence Score
--     CIViC_Ent_Type TEXT, --CIViC Entity Type
--     CIViC_Ent_ID VARCHAR(30), --CIViC Entity ID
--     CIViC_Ent_URL TEXT, --CIViC Entity URL
--     CIViC_Ent_Src VARCHAR(20), --CIViC Entity Source -- 
--     CIViC_Ent_Var_Origin VARCHAR(20), -- CIViC Entity Variant Origin SOMATIC/GENETIC, rare_Germlıne
--     CIViC_Ent_Stat VARCHAR(30), --CIViC Entity Status accepted,submitted
--     CIViC_Clin_Sig VARCHAR(30), --CIViC Entity Clinical Significance
--     CIViC_Ent_Dir TEXT, --CIViC Entity Direction supports
--     CIViC_Ent_Disease TEXT, --CIViC Entity Diseasethe disease should be the cancer or cancer subtype that is a result of the described variant. 
--     CIViC_Ent_Drugs TEXT, --CIViC Entity Drugs Drugs in CIViC are associated with Predictive Evidence Types, which describe sensitivity, resistance or adverse response to drugs when a given variant is present. 
--     CIViC_Ent_Drug_Int TEXT, --CIViC Entity Drug Interaction Type
--     CIViC_Ev_Phenotypes TEXT, --CIViC Evidence Phenotypes
--     CIViC_Ev_Level TEXT, --CIViC Evidence Level
--     CIViC_Ev_Rating TEXT, --CIViC Evidence Rating
--     CIViC_Assertion_ACMG_Codes TEXT, --CIViC Assertion ACMG Codes
--     CIViC_Assertion_AMP_Cat TEXT, --CIViC Assertion AMP Category
--     CIViC_Assertion_NCCN_Guid TEXT, --CIViC Assertion AMP Category
--     CIViC_Assertion_Regu_Appr_Guid TEXT, --CIVIC Assertion Regulatory Approval
--     CIViC_Assertion_FDA_Comp_Test_Guid TEXT --CIVIC Assertion FDA Companion Test 
-- );





select * from civic_variants where alt='GGCAGCTGGTGCT';
select (CHROM,	POS,	VAR_ID,	REF,	ALT,	QUAL,	FILTER) from civic_variants where alt='GGCAGCTGGTGCT';
select (CHROM,	POS,	VAR_ID,	REF,	ALT,	QUAL,	FILTER) from civic_variants where chrom='1';
select (CHROM,	POS,	VAR_ID,	REF,	GN,	QUAL,	VT, Allele, Consequence) from civic_variants;
select GN from civic_variants where CHROM='1'	and POS='11187094'	and REF='G' and ALT='T';

