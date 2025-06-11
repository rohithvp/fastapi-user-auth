from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url =  "postgresql://postgres:password@172.17.0.1:5432/users"

engine= create_engine(database_url)

sessionlocal= sessionmaker(autocommit=False,autoflush=False ,bind=engine)

Base =  declarative_base()