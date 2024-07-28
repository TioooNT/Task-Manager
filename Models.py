import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


engine = create_engine('mariadb+pymysql://root:5040@localhost/TaskManager')


Session = sessionmaker(bind=engine)
session = Session()
