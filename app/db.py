from sqlalchemy import create_engine, Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


DATABASE = 'sqlite:///db.sqlite'

engine = create_engine(DATABASE)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


project_users_table = Table('project_users_table', Base.metadata,
                            Column('project_id', Integer, ForeignKey('projects.id')),
                            Column('user_id', Integer, ForeignKey('users.id'))
                            )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('User', secondary=project_users_table, backref='projects')
    cases = relationship('Case', backref='project')


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'))

    branches = relationship('Branch', backref='case')


class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    case_id = Column(Integer, ForeignKey('cases.id'))

    pipes = relationship('Pipe', backref='branch')


class Pipe(Base):
    __tablename__ = 'pipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    branch_id = Column(Integer, ForeignKey('branches.id'))


class NaePals(Base):
    __tablename__ = 'naepals'
    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(engine)