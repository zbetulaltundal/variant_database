CREATE TABLE variant(
    ID  SERIAL PRIMARY KEY, 
    CHROM  TEXT NOT NULL,--an identifier from the reference genome. All entries for a specific CHROM should form a contiguous block within the VCF file.(Alphanumeric String, Required)
    POS INT NOT NULL,-- Positions are sorted numerically, in increasing order, within each reference sequence CHROM. (Integer, Required)
    VAR_ID TEXT, -- The identifier of the variation, ??? same as DBSNPİD??
    REF TEXT,
    ALT TEXT, --Alternation
    QUAL TEXT, -- 
    FILTER TEXT,
    INFO TEXT
)