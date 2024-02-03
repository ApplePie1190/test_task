import os
from environs import Env

env = Env()
env.read_env()

HOST = env.str('HOST')
USER = env.str('USER')
PASSWORD = env.str('PASSWORD')
DB = env.str('DB')
SECRET_KEY = env.str('SECRET_KEY')
URI = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'


class BaseConfig:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = URI


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = URI
