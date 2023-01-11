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
