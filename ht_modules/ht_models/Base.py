print("- in modelsBase")
from sqlalchemy import create_engine, inspect
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from .config import config
import os


Base_users = declarative_base()


dict_base = {}
dict_base["Base_users"]=Base_users


engine_users = create_engine(config.SQL_URI_USERS)

dict_engine = {}
dict_engine["engine_users"]=engine_users


SessionUsers = sessionmaker(bind = engine_users)


sess_users = SessionUsers()

dict_sess = {}
dict_sess["sess_users"]=sess_users




