import os
from dotenv import load_dotenv

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:mumel0615@localhost/agendamentos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    load_dotenv()