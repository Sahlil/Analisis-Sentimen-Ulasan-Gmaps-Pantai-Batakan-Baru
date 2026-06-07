import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

class Config:
    # URL database dijadikan satu baris agar tidak ada error spasi (IndentationError)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://sahlilmy_rs:jG0FIcaDZ%Xl6Mwm@localhost/sahlilmy_tadb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'asdqwe123')
