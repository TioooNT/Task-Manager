import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


engine = create_engine('mariadb+pymysql://tiooo:5040@localhost:3306/TaskManager')

Session = sessionmaker(bind=engine)
session = Session()
