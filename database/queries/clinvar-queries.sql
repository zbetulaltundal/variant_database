-- v.1.0

select CHROM, POS, REF, ALT, QUAL, FILTER  from variant;

SELECT * FROM INFO WHERE id IN 
   (SELECT id FROM variant 
      WHERE ALT='{ALT}' AND
            REF='{REF}' AND
            POS='{POS}' AND
            CHROM='{CHROM}')

select CHROM, POS, REF, ALT  from variant;

SELECT * FROM INFO WHERE id IN 
   (SELECT INFO_ID FROM variant 
      WHERE ALT='A' AND
            REF='G' AND
            POS='925952' AND
            CHROM='1');

SELECT ABBRV FROM CLNDISDB_ABBRV WHERE ID IN
  (SELECT CLNDISDB_NAME_ID FROM CLNDISDB 
    WHERE INFO_ID IN 
    (SELECT INFO_ID FROM variant 
        WHERE ALT='A' AND
              REF='G' AND
              POS='925952' AND
              CHROM='1') );

SELECT CLNDISDB_NAME,CLNDISDB_ID FROM CLNDISDB WHERE INFO_ID IN 
   (SELECT INFO_ID FROM variant 
      WHERE ALT='A' AND
            REF='G' AND
            POS='925952' AND
            CHROM='1');

SELECT CLNSIG FROM CLNSIG WHERE INFO_ID IN 
   (SELECT INFO_ID FROM variant 
      WHERE ALT='A' AND
            REF='G' AND
            POS='925952' AND
            CHROM='1');

SELECT CLNSIG FROM CLNSIG WHERE INFO_ID IN 
   (SELECT INFO_ID FROM variant 
      WHERE ALT='A' AND
            REF='G' AND
            POS='925952' AND
            CHROM='1');

drop table INFO;
drop table VARIANT;
drop table CLNDISDB_ABBRV;
drop table CLNDISDB;
drop table CLNSIG;
drop table CLNSIGCONF;
drop table CLNSIGINCL;
drop table MC;
drop table GENEINFO;
drop table CLNREVSTAT;
drop table CLNVI;
drop table CLNDN;
drop table CLNDNINCL;

alter table INFO  DISABLE TRIGGER ALL;
alter table INFO DISABLE TRIGGER ALL;
alter table CLNDISDB_ABBRV DISABLE TRIGGER ALL;
alter table CLNDISDB DISABLE TRIGGER ALL;
alter table CLNSIG DISABLE TRIGGER ALL;
alter table CLNSIGCONF DISABLE TRIGGER ALL;
alter table CLNSIGINCL DISABLE TRIGGER ALL;
alter table MC DISABLE TRIGGER ALL;
alter table GENEINFO DISABLE TRIGGER ALL;
alter table CLNREVSTAT DISABLE TRIGGER ALL;
alter table CLNVI DISABLE TRIGGER ALL;
alter table CLNDN DISABLE TRIGGER ALL;
alter table CLNDNINCL DISABLE TRIGGER ALL;

delete from INFO;
delete from variant;
delete from CLNDISDB_ABBRV;
delete from CLNDISDB;
delete from CLNSIG;
delete from CLNSIGCONF;
delete from CLNSIGINCL;
delete from MC;
delete from GENEINFO;
delete from CLNREVSTAT;
delete from CLNVI;
delete from CLNDN;
delete from CLNDNINCL;

# v1

CREATE TABLE CLNDISDB_ABBRV (
  ID  SERIAL PRIMARY KEY,
  NAME TEXT,
  ABBRV TEXT
);

CREATE TABLE CLNDISDB (
    ID  SERIAL PRIMARY KEY,
    CLNDISDB_NAME_ID INT,--"Tag-value pairs of disease database name and identifier, e.g. OMIM:NNNNNN">
    CLNDISDB_NAME TEXT,
    CLNDISDB_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNDISDB
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_CLNDISDB_abbrv
      FOREIGN KEY(CLNDISDB_NAME_ID) 
	      REFERENCES CLNDISDB_ABBRV(ID)
);

CREATE TABLE CLNSIG (
    ID  SERIAL PRIMARY KEY, 
    CLNSIG TEXT, --Clinical significance for this single variant; multiple values are separated by a vertical bar
    INFO_ID INT,
    CONSTRAINT fk_CLNSIG
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Conflicting clinical significance for this single variant; multiple values are separated by a vertical bar
CREATE TABLE CLNSIGCONF(
    ID  SERIAL PRIMARY KEY, 
    CLNSIGCONF TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNSIGCONF
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Clinical significance for a haplotype or genotype that includes this variant. Reported as pairs of VariationID:clinical significance; multiple values are separated by a vertical bar
CREATE TABLE CLNSIGINCL(
    ID  SERIAL PRIMARY KEY, 
    CLNSIGINCL TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNSIGINCL
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--comma separated list of molecular consequence in the form of Sequence Ontology ID|molecular_consequence
CREATE TABLE MC(
    ID  SERIAL PRIMARY KEY, 
    Seq_Ont_ID TEXT,
    Mol_Conseq TEXT,
    INFO_ID INT,
    CONSTRAINT fk_MC
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--Gene(s) for the variant reported as gene symbol:gene id. The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
CREATE TABLE GENEINFO(
    ID  SERIAL PRIMARY KEY, 
    Gene_Sym TEXT,
    Gene_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_GENEINFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--ClinVar review status for the Variation ID
CREATE TABLE CLNREVSTAT(
    ID  SERIAL PRIMARY KEY, 
    STAT TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNREVSTAT
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

CREATE TABLE CLNVI(
    ID  SERIAL PRIMARY KEY, 
    SRC TEXT,
    SRC_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNVI
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--ClinVar's preferred disease name for the concept specified by disease identifiers in CLNDISDB    
CREATE TABLE CLNDN(
    ID  SERIAL PRIMARY KEY, 
    DISEASE_NAME TEXT,
    DISEASE_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNDN
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

--For included Variant : ClinVar's preferred disease name for the concept specified by disease identifiers in CLNDISDB    
CREATE TABLE CLNDNINCL(
    ID  SERIAL PRIMARY KEY, 
    DISEASE_NAME TEXT,
    DISEASE_ID TEXT,
    INFO_ID INT,
    CONSTRAINT fk_CLNDNINCL
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
        ON DELETE CASCADE
);

CREATE TABLE INFO(
    ID  SERIAL PRIMARY KEY, 
    AF_ESP NUMERIC,
    AF_EXAC NUMERIC,
    AF_TGP NUMERIC,
    ALLELEID INT,
    CLNHGVS TEXT,
    CLNVC TEXT, --Variant type +
    CLNVCSO TEXT, --Sequence Ontology id for variant type +
    DBVARID TEXT, --nsv accessions from dbVar for the variant
    ORIGIN TEXT, --Allele origin. One or more of the following values may be added: 0 - unknown; 1 - germline; 2 - somatic; 4 - inherited; 8 - paternal; 16 - maternal; 32 - de-novo; 64 - biparental; 128 - uniparental; 256 - not-tested; 512 - tested-inconclusive; 1073741824 - other
    RS TEXT, --dbSNP ID (i.e. rs number)
    SSR INT --Variant Suspect Reason Codes. One or more of the following values may be added: 0 - unspecified, 1 - Paralog, 2 - byEST, 4 - oldAlign, 8 - Para_EST, 16 - 1kg_failed, 1024 - other
);

CREATE TABLE VARIANT (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,-- An identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS  INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    CLINVAR_ID TEXT, -- ClinVar Variation ID"+
    REF TEXT,
    ALT TEXT,
    QUAL NUMERIC,
    FILTER TEXT,
    INFO_ID INT,
    CONSTRAINT fk_INFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
);

-- create domain ALT as TEXT check (value !~ '[\t\v\b\r\n\cd95\cd94\2c]');


-- v2.0

CREATE TABLE variants (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,-- An identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS  INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    CLINVAR_ID TEXT, -- ClinVar Variation ID"+
    REF TEXT,
    ALT TEXT,
    QUAL NUMERIC,
    FILTER TEXT,
    AF_ESP NUMERIC,
    AF_EXAC NUMERIC,
    AF_TGP NUMERIC,
    ALLELEID INT,
    CLNHGVS TEXT,
    CLNVC TEXT, --Variant type +
    CLNVCSO TEXT, --Sequence Ontology id for variant type +
    DBVARID TEXT, --nsv accessions from dbVar for the variant
    ORIGIN TEXT, --Allele origin. One or more of the following values may be added: 0 - unknown; 1 - germline; 2 - somatic; 4 - inherited; 8 - paternal; 16 - maternal; 32 - de-novo; 64 - biparental; 128 - uniparental; 256 - not-tested; 512 - tested-inconclusive; 1073741824 - other
    RS TEXT, --dbSNP ID (i.e. rs number)
    SSR INT --Variant Suspect Reason Codes. One or more of the following values may be added: 0 - unspecified, 1 - Paralog, 2 - byEST, 4 - oldAlign, 8 - Para_EST, 16 - 1kg_failed, 1024 - other
    CLNDNINCL_DISEASE_NAME TEXT,
    CLNDNINCL_DISEASE_ID TEXT,
    CLNDN_DISEASE_NAME TEXT,
    CLNDN_DISEASE_ID TEXT,
    CLNVI TEXT,
    CLNREVSTAT TEXT,
    GENEINFO TEXT, --Gene(s) for the variant reported as gene symbol:gene id. The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
    Molecular_Consequence TEXT,--comma separated list of molecular consequence in the form of Sequence Ontology ID|molecular_consequence
    CLNSIGINCL TEXT,
    CLNSIGCONF TEXT,
    CLNSIG TEXT, -- Clinical significance for this single variant; multiple values are separated by a vertical bar
    CLNDISDB TEXT, -- --"Tag-value pairs of disease database name and identifier, e.g. OMIM:NNNNNN">
    ABBRV TEXT
);


-- v3 last
CREATE TABLE INFO(
    ID  SERIAL PRIMARY KEY, 
    AF_ESP NUMERIC,
    AF_EXAC NUMERIC,
    AF_TGP NUMERIC,
    ALLELEID INT,
    CLNHGVS TEXT,
    CLNVC TEXT, --Variant type +
    CLNVCSO TEXT, --Sequence Ontology id for variant type +
    DBVARID TEXT, --nsv accessions from dbVar for the variant
    ORIGIN TEXT, --Allele origin. One or more of the following values may be added: 0 - unknown; 1 - germline; 2 - somatic; 4 - inherited; 8 - paternal; 16 - maternal; 32 - de-novo; 64 - biparental; 128 - uniparental; 256 - not-tested; 512 - tested-inconclusive; 1073741824 - other
    RS TEXT, --dbSNP ID (i.e. rs number)
    SSR INT --Variant Suspect Reason Codes. One or more of the following values may be added: 0 - unspecified, 1 - Paralog, 2 - byEST, 4 - oldAlign, 8 - Para_EST, 16 - 1kg_failed, 1024 - other
);

CREATE TABLE VARIANT (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,-- An identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS  INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    CLINVAR_ID TEXT, -- ClinVar Variation ID"+
    REF TEXT,
    ALT TEXT,
    QUAL NUMERIC,
    FILTER TEXT,
    INFO_ID INT,
    CONSTRAINT fk_INFO
      FOREIGN KEY(INFO_ID) 
	      REFERENCES INFO(ID)
);

-- create domain ALT as TEXT check (value !~ '[\t\v\b\r\n\cd95\cd94\2c]');


-- v2.0

CREATE TABLE variants (
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,-- An identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS  INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    CLINVAR_ID TEXT, -- ClinVar Variation ID"+
    REF TEXT,
    ALT TEXT,
    QUAL NUMERIC,
    FILTER TEXT,
    AF_ESP NUMERIC,
    AF_EXAC NUMERIC,
    AF_TGP NUMERIC,
    ALLELEID INT,
    CLNHGVS TEXT,
    CLNVC TEXT, --Variant type +
    CLNVCSO TEXT, --Sequence Ontology id for variant type +
    DBVARID TEXT, --nsv accessions from dbVar for the variant
    ORIGIN TEXT, --Allele origin. One or more of the following values may be added: 0 - unknown; 1 - germline; 2 - somatic; 4 - inherited; 8 - paternal; 16 - maternal; 32 - de-novo; 64 - biparental; 128 - uniparental; 256 - not-tested; 512 - tested-inconclusive; 1073741824 - other
    RS TEXT, --dbSNP ID (i.e. rs number)
    SSR INT --Variant Suspect Reason Codes. One or more of the following values may be added: 0 - unspecified, 1 - Paralog, 2 - byEST, 4 - oldAlign, 8 - Para_EST, 16 - 1kg_failed, 1024 - other
    CLNDNINCL_DISEASE_NAME TEXT,
    CLNDNINCL_DISEASE_ID TEXT,
    CLNDN_DISEASE_NAME TEXT,
    CLNDN_DISEASE_ID TEXT,
    CLNVI TEXT,
    CLNREVSTAT TEXT,
    GENEINFO TEXT, --Gene(s) for the variant reported as gene symbol:gene id. The gene symbol and id are delimited by a colon (:) and each pair is delimited by a vertical bar (|)
    Molecular_Consequence TEXT,--comma separated list of molecular consequence in the form of Sequence Ontology ID|molecular_consequence
    CLNSIGINCL TEXT,
    CLNSIGCONF TEXT,
    CLNSIG TEXT, -- Clinical significance for this single variant; multiple values are separated by a vertical bar
    CLNDISDB TEXT, -- --"Tag-value pairs of disease database name and identifier, e.g. OMIM:NNNNNN">
    ABBRV TEXT
);