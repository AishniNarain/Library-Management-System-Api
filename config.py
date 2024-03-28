#Adding configurations to the main application
from datetime import timedelta

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/library_api'
JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=2)