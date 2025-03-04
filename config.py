import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
