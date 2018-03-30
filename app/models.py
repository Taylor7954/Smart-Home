
# ===STD Imports
from os import environ

# ===PIP IMPORTS
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from sshtunnel import SSHTunnelForwarder

Base = declarative_base()

class User(Base):

    __tablename__ = 'capstone_users'

    id = Column(Integer, primary_key=True)
    # username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    # name used to greet user
    name = Column(Text, nullable=False)

    houses = relationship('capstone_homes', backref='capstone_users', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Houses are the main relation of the application
class Home(Base):

    __tablename__ = 'capstone_homes'

    id = Column(Integer, primary_key = True)

    account_id = Column(Integer, ForeignKey('capstone_users.id'), nullable=False)

    street_address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip_code = Column(Integer)

    rooms = relationship('Room', backref='home', lazy=True)

# create sshtunnel
server = SSHTunnelForwarder(
    'lan.cis.uab.edu',
    ssh_username='smso3223',
    # ssh_pkey="~/.ssh/id_rsa",
    ssh_password='Thefoxranupthetree33',
    # local_bind_address=('localhost', 10_000),
    remote_bind_address=('cisdb.cis.uab.edu', 5432)
)

server.start()
local_port = server.local_bind_port

db_uri = f'postgres://smso3223:Thefoxranupthetree33@127.0.0.1:{local_port}/smso3223'
# db_uri = f'postgres://wjsetzer:EnLgKLzj@127.0.0.1:5432/infinitechan'
engine = create_engine(db_uri)

if not engine.dialect.has_table(engine, User.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

