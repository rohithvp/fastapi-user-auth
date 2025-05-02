from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url =  "postgresql://postgres:postgres@172.17.0.3:5432/user_auth_db"

engine= create_engine(database_url)

sessionlocal= sessionmaker(autocommit=False,autoflush=False ,bind=engine)

Base =  declarative_base()