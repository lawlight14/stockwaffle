import os
from datetime import timedelta

class Config(object):
    # Set secret key to use session
    SECRET_KEY = "likelion-flaskr-secret-key"
    debug = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "14eterna@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///swdb?instance=lavisividb:lavisdb'
    migration_directory = 'migrations'

