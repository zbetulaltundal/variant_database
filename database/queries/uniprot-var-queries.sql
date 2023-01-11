

--evidence:-- comma sep list '-' (dash) means no value in Ensembl Variation.
CREATE TABLE VARIANT(
    ID bigserial PRIMARY KEY,
    gene_name TEXT, -- GENE_SYMBOL
    AC TEXT,--UniProtKB accession for the entry
    variant_aa_change TEXT,
    source_db_id TEXT, --dbSNP identifier
    consequence_type TEXT,   
    clinical_significance TEXT, -- comma sep list '-' (dash) means no value in Ensembl Variation.
    phenotype_disease TEXT,  --'-' (dash) means no value in Ensembl Variation.
    phenotype_disease_source TEXT, --'-' (dash) means no value in Ensembl Variation.
    cytogenetic_band TEXT,
    chromosome_coordinate TEXT, --Chromosome and base pair (bp) coordinate eg 19:g.58864491G>A
    ensembl_gene_ID TEXT,
    ensembl_transcript_ID TEXT,
    ensembl_translation_ID TEXT
);

CREATE TABLE EVIDENCE (
    ID bigserial PRIMARY KEY,
    evidence_name TEXT,
    variant_id INT,
    CONSTRAINT fk_VARIANT
      FOREIGN KEY(variant_id) 
	      REFERENCES VARIANT(ID)
);
