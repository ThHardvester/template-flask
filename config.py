import os

class Config:
    SECRET_KEY = '11234567890qwertyuiop'  # Cambia esto por una clave segura
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

