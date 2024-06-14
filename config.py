#Adding configurations to the main application
from datetime import timedelta
import os

SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:RootPass5!@localhost:3306/library_api'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://remote_user:password@172.17.0.1:3307/dbname'
# SQLALCHEMY_DATABASE_URI =  os.environ['DATABASE_URL']
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:RootPass5!@msyql-db:3306/dbname'
JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'aishninarain2000@gmail.com'
MAIL_PASSWORD = 'tqpa avpq wvrt dpfk'
MAIL_USE_TLS = False
MAIL_USE_SSL = True