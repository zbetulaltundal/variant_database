
-- ClinicalAnnotationID 9 bsamaklı sayı
-- Genotype/Allele string 
-- Annotation Text
-- allele Function

-- drugs seperated by , ; / which means what 
CREATE TABLE DRUG (
    ID bigserial PRIMARY KEY,
    DRUG TEXT
);

CREATE TABLE PHENOTYPE (
    ID bigserial PRIMARY KEY,
    PHENOTYPE_NAME TEXT
);

CREATE TABLE pharmgkb (
    ID bigserial PRIMARY KEY,
    Clinical_Annotation_ID TEXT, -- 'Clinical Annotation ID'
    VARIANT TEXT, -- 'Variant/Haplotypes'
    GENE TEXT, -- 'Gene'
    LEVEL_OF_EVIDENCE TEXT, -- 'Level of Evidence'
    LEVEL_OVERRIDE TEXT, --  'Level Override'
    LEVEL_MODIFIERS TEXT, -- 'Level Modifiers'
    SCORE TEXT, --  'Score_x'
    PHENOTYPE_CATEGORY TEXT, --'Phenotype Category'
    PMID_COUNT TEXT, -- 'PMID Count'
    EVIDENCE_COUNT TEXT, -- 'Evidence Count'
    LATEST_HISTORY_DATE DATE, -- 'Latest History Date (YYYY-MM-DD)'
    pharmgkb_URL TEXT, -- 'URL'
    Specialty_Population TEXT, --  'Specialty Population'
    Genotype TEXT, -- 'Genotype/Allele'
    ANNOTATION_TEXT TEXT, -- 'Annotation Text'
    Allele_Function TEXT, -- 'Allele Function'
    Evidence_ID TEXT, -- 'Evidence ID'
    Evidence_Type TEXT, -- 'Evidence Type'
    Evidence_URL TEXT, -- 'Evidence URL'
    Evidence_PMID TEXT, -- 'PMID'
    Evidence_Summary TEXT, --  'Summary'
    Evidence_Score TEXT, --  'Score_y'
    DRUG_ID BIGINT,
    PHENOTYPE_ID BIGINT,
    CONSTRAINT fk_DRUG
      FOREIGN KEY(DRUG_ID) 
	      REFERENCES DRUG(ID),
    CONSTRAINT fk_PHENOTYPE
      FOREIGN KEY(PHENOTYPE_ID) 
	      REFERENCES PHENOTYPE(ID)
);