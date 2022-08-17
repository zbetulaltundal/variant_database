
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
CLINVAR_DB_NAME = 'clinvar'
CIVIC_DB_NAME = 'CIVic'
DB_PWD = 'test'
ALLOWED_EXTENSIONS = {'vcf'}
UPLOAD_FOLDER = f'{path}\\files\\'
# DSN = f"user='{USER_NAME}' password='{HOST_NAME}' host='{HOST_NAME}' port='{PORT_NAME}'"
