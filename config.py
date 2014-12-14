import os

class BaseConfig(object): 
  SECRET_KEY = "kjdsbfkjgdf78sft"
  #SQLALCHEMY_DATABASE_URI = "postgresql://localhost/dev"
  #SQLALCHEMY_DATABASE_URI = 'postgres://egcvfsjbvayonq:mU266saTkSwflOPxo6nFNb_OUk@ec2-54-197-237-120.compute-1.amazonaws.com:5432/d6ol2sbr6c9gjf'
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
  