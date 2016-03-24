from sqlalchemy import create_engine, Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
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

# Time to get a little trickier for our little mapper

#
#   O--->O--->O
#   ^         v
#   O<---O<---O
#   ^    ^    v
#   O<---O<---O
#


class TopLeft(Base):
    __tablename__ = 'top-lefts'
    id = Column(Integer, primary_key=True)
    top_mid_id = Column(Integer, ForeignKey('top-mids.id'))
    top_mid = relationship('TopMid', backref=backref('top_left', uselist=False))

class TopMid(Base):
    __tablename__ = 'top-mids'
    id = Column(Integer, primary_key=True)
    top_right_id = Column(Integer, ForeignKey('top-rights.id'))
    top_right = relationship('TopRight', backref=backref('top_mid', uselist=False))

class TopRight(Base):
    __tablename__ = 'top-rights'
    id = Column(Integer, primary_key=True)
    mid_right_id = Column(Integer, ForeignKey('mid-rights.id'))
    mid_right = relationship('MidRight', backref=backref('top_right', uselist=False))

class MidLeft(Base):
    __tablename__ = 'mid-lefts'
    id = Column(Integer, primary_key=True)
    top_left_id = Column(Integer, ForeignKey('top-lefts.id'))
    top_left = relationship('TopLeft', backref=backref('mid_left', uselist=False))

class MidMid(Base):
    __tablename__ = 'mid-mids'
    id = Column(Integer, primary_key=True)
    mid_left_id = Column(Integer, ForeignKey('mid-lefts.id'))
    mid_left = relationship('MidLeft', backref=backref('mid_mid', uselist=False))

class MidRight(Base):
    __tablename__ = 'mid-rights'
    id = Column(Integer, primary_key=True)
    bottom_right_id = Column(Integer, ForeignKey('bottom-rights.id'))
    bottom_right = relationship('BottomRight', backref=backref('mid_right', uselist=False))
    mid_mid_id = Column(Integer, ForeignKey('mid-mids.id'))
    mid_mid = relationship('MidMid', backref=backref('mid_right', uselist=False))

class BottomLeft(Base):
    __tablename__ = 'bottom-lefts'
    id = Column(Integer, primary_key=True)
    mid_left_id = Column(Integer, ForeignKey('mid-lefts.id'))
    mid_left = relationship('MidLeft', backref=backref('bottom_left', uselist=False))

class BottomMid(Base):
    __tablename__ = 'bottom-mids'
    id = Column(Integer, primary_key=True)
    bottom_left_id = Column(Integer, ForeignKey('bottom-lefts.id'))
    bottom_left = relationship('BottomLeft', backref=backref('bottom_mid', uselist=False))
    mid_mid_id = Column(Integer, ForeignKey('mid-mids.id'))
    mid_mid = relationship('MidMid', backref=backref('bottom_mid', uselist=False))

class BottomRight(Base):
    __tablename__ = 'bottom-rights'
    id = Column(Integer, primary_key=True)
    bottom_mid_id = Column(Integer, ForeignKey('bottom-mids.id'))
    bottom_mid = relationship('BottomMid', backref=backref('bottom_right', uselist=False))


Base.metadata.create_all(engine)