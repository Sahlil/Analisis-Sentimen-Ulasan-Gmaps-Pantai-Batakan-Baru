import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/ta_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kunci_rahasia_skripsi_kamu'