
"""Flask configuration."""
from os import path

FLASK_ENV = 'development'
TESTING = True
SECRET_KEY = "KPC4LKd7KvF0nRPGpvmv3Q"
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'
DB_USER = 'postgres'
HOST_NAME = 'localhost'
PORT_NAME = '5432'
DB_PWD = 'test'
DB_STRING = f"postgres://{DB_USER}:{DB_PWD}@{HOST_NAME}:{PORT_NAME}"

CLINVAR_DB_NAME = 'clinvar'
CIVIC_DB_NAME = 'civic'


USER_DB_NAME = 'userdb'
ALLOWED_EXTENSIONS = {'vcf'}

DICT_EXCEL_PATH = 'sozluk.xlsx'

