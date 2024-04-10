#Adding configurations to the main application
from datetime import timedelta
import os

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/library_api'
JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'aishninarain2000@gmail.com'
MAIL_PASSWORD = 'tqpa avpq wvrt dpfk'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

