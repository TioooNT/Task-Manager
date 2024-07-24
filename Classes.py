from Models import engine, session
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'user'
    
    full_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(12))
    password: Mapped[str] = mapped_column(String(25))
    task: Mapped[List['Task']] = relationship(back_populates='author')


class Category(Base):
    __tablename__ = 'category'
    
    subject: Mapped[str] = mapped_column(String(25))


class Task(Base):
    __tablename__ = 'task'
    
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(255))
    author: Mapped['User'] = relationship(back_populates='task')
    category: Mapped[str] = mapped_column(ForeignKey('category.subject'))
    status: Mapped[bool] = mapped_column(default=False)


Tiooo = User(full_name='Bao Tran Gia', username='tiooo', password='Yajin2008')
session.commit()

Maths = Category(subject='Maths')
session.commit()

Task(title='Task manager', content='Create a task managing console application', author = Tiooo, category = 'Maths')
session.commit()