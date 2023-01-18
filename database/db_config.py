# database configuration
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PWD = "test"
CLINGEN_DB_NAME = "clingen"
CIVIC_DB_NAME ='civic'
CLINVAR_DB_NAME ='clinvar'
PHARMGKB_DB_NAME ='pharmgkb'
UNIPROTVAR_DB_NAME ='uniprot'
PORT_NAME = '5432'
DB_STRING = f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{PORT_NAME}"
