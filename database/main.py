''' @author: Zeynep Betül Altundal
how to run?
python main.py --dbname=<dataset name>
dataset name options: civic, clingen, clinvar, pharmgkb, uniprot
example:
python main.py --dbname=clinvar

'''
import argparse

from clinvar_import import(
    import_clinvar_data
)

from civic_import import(
    import_civic_data
)

from clingen_import import(
    import_clingen_data
)

from pharmgkb_import import(
    import_pharmgkb
)

from uniprot_var_import import(
    import_uniprot
)

import db_config

from db_utils import(
    db_connect
)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dbname', 
        metavar='db',
        type=str, 
        default="uniprot",
        help=f'name of database: clinvar, civic, clingen, pharmgkb, uniprot',
    )
    
    args = parser.parse_args()
    print(args)
    conn = None
    if args.dbname == "civic":
        conn = db_connect(db_config.CIVIC_DB_NAME)
        import_civic_data(conn)
    elif args.dbname == "clingen":   
        conn = db_connect(db_config.CLINGEN_DB_NAME)
        import_clingen_data(conn)
    elif args.dbname == "clinvar":   
        conn = db_connect(db_config.CLINVAR_DB_NAME)
        import_clinvar_data(conn)
    elif args.dbname == "pharmgkb":   
        conn = db_connect(db_config.PHARMGKB_DB_NAME)
        import_pharmgkb(conn)
    elif args.dbname == "uniprot":   
        conn = db_connect(db_config.UNIPROTVAR_DB_NAME)
        import_uniprot(conn)
    if conn:
        conn.close()
        