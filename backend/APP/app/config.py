import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:serpent00@host.docker.internal:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#'mysql+pymysql://root:serpent00@localhost:3306/test' for running outside the container