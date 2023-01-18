
CREATE TABLE INFO (
    ID  SERIAL PRIMARY KEY, 
    ALLELEID TEXT,
    CLNHGVS TEXT,
    CLNVC TEXT, --Variant type +
    CLNVCSO TEXT, --Sequence Ontology id for variant type +
    ORIGIN TEXT, --Allele origin. One or more of the following values may be added: 0 - unknown; 1 - germline; 2 - somatic; 4 - inherited; 8 - paternal; 16 - maternal; 32 - de-novo; 64 - biparental; 128 - uniparental; 256 - not-tested; 512 - tested-inconclusive; 1073741824 - other
    AF_ESP TEXT,
    AF_EXAC TEXT,
    AF_TGP TEXT,
    DBVARID TEXT, --nsv accessions from dbVar for the variant
    RS TEXT, --dbSNP ID (i.e. rs number)
    SSR TEXT --Variant Suspect Reason Codes. One or more of the following values may be added: 0 - unspecified, 1 - Paralog, 2 - byEST, 4 - oldAlign, 8 - Para_EST, 16 - 1kg_failed, 1024 - other);
);

CREATE TABLE CLNDISDB ( --+
    ID  SERIAL PRIMARY KEY,
    CLNDISDB_NAME TEXT,
    CLNDISDB_ABBRV TEXT,
    CLNDISDB_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNDISDB
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Gene(s) for the variant reported as gene symbol:gene id. 
--The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
CREATE TABLE GENEINFO( --+
    ID  SERIAL PRIMARY KEY, 
    GENE_SYMBOL TEXT,
    GENE_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_GENEINFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

CREATE TABLE CLNVI( --+
    ID  SERIAL PRIMARY KEY, 
    SRC TEXT,
    SRC_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNVI
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--comma separated list of molecular consequence in the form of Sequence Ontology ID|molecular_consequence
CREATE TABLE MC( --+
    ID  SERIAL PRIMARY KEY, 
    sequence_ontology_id TEXT,
    molecular_consequence TEXT,
    INFO_ID INT,
    CONSTRAINT fk_MC
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

CREATE TABLE CLNSIG (--+
    ID  SERIAL PRIMARY KEY, 
    CLNSIG TEXT, --Clinical significance for this single variant; multiple values are separated by a vertical bar
    INFO_ID INT,
    CONSTRAINT fk_CLNSIG
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Conflicting clinical significance for this single variant; multiple values are separated by a vertical bar
CREATE TABLE CLNSIGCONF(--+
    ID  SERIAL PRIMARY KEY, 
    CLNSIGCONF TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNSIGCONF
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Clinical significance for a haplotype or genotype that includes this variant. Reported as pairs of VariationID:clinical significance; multiple values are separated by a vertical bar
CREATE TABLE CLNSIGINCL(--+
    ID  SERIAL PRIMARY KEY, 
    CLNSIGINCL TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNSIGINCL
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);


--Gene(s) for the variant reported as gene symbol:gene id. The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
CREATE TABLE CLNDN(
    ID  SERIAL PRIMARY KEY, 
    CLNDN_GENE_SYMBOL TEXT,
    CLNDN_GENE_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_GENEINFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

-- Gene(s) for the variant reported as 
-- gene symbol:gene id. 
-- The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
CREATE TABLE CLNDNINCL(
    ID  SERIAL PRIMARY KEY, 
    CLNDNINCL_GENE_SYMBOL TEXT,
    CLNDNINCL_GENE_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_GENEINFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);


--ClinVar review status for the Variation ID
CREATE TABLE CLNREVSTAT( --+
    ID  SERIAL PRIMARY KEY, 
    REVIEW_STATUS TEXT,
    NUM_OF_SUBMITTERS TEXT,
    CONFLICT TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNREVSTAT
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);



CREATE TABLE VARIANT (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,-- An identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS  INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    CLINVAR_ID TEXT, -- ClinVar Variation ID"+
    REF TEXT,
    ALT TEXT,
    QUAL TEXT,
    FILTER TEXT,
    INFO_ID INT,
    CONSTRAINT fk_INFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);
