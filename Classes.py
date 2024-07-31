import datetime
from Models import engine, session
from typing import List
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass
    

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    full_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(12))
    password: Mapped[str] = mapped_column(String(25))

    tasks: Mapped[List["Task"]] = relationship()
    
    categories: Mapped[List["Category"]] = relationship()


class Category(Base):
    __tablename__ = 'category'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(25))

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author: Mapped[User] = relationship(back_populates='categories')

    tasks: Mapped[List["Task"]] = relationship()


class Task(Base):
    __tablename__ = 'task'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(255))

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author: Mapped[User] = relationship(back_populates='tasks')

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='tasks')
    
    status: Mapped[bool] = mapped_column(default=False)
    dateAdded: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())


