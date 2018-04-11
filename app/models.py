
# ===STD Imports
# from os import environ

# ===PIP IMPORTS
from sqlalchemy import Column, DateTime, Boolean, Float, Integer, String, Text, ForeignKey
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

    homes = relationship('Home', backref='capstone_users', lazy=True)

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

    latitude = Column(Float)
    longitude = Column(Float)

    rooms = relationship('Room', backref='capstone_homes', lazy=True)

class Room(Base):

    __tablename__ = 'capstone_rooms'

    id = Column(Integer, primary_key = True)

    home_id = Column(Integer, ForeignKey('capstone_homes.id'), nullable=False)

    name = Column(Text, nullable=False)

    # define lights and entry points for room
    # cascade means that if the room is deleted, so are they
    rooms = relationship('Light', backref='capstone_rooms', cascade="all,delete", lazy=True)
    rooms = relationship('EntryPoint', backref='capstone_rooms', cascade="all,delete", lazy=True)

class Light(Base):

    __tablename__ = 'capstone_lights'

    id = Column(Integer, primary_key=True)

    room_id = Column(Integer, ForeignKey('capstone_rooms.id'), nullable=False)

    # room name can be queried from the DB
    # specify default name?
    name = Column(Text)
    is_on = Column(Boolean)

    def __repr__(self):
        return f'<Light {self.room}: {self.name}>'

class EntryPoint(Base):

    __tablename__ = 'capstone_entry_points'

    id = Column(Integer, primary_key=True)

    room_id = Column(Integer, ForeignKey('capstone_rooms.id'), nullable=False)

    name = Column(Text)
    is_open = Column(Boolean)

class ThingTracker(Base):

    __tablename__ = 'capstone_thing_tracker'

    # NOTE: pretty sure the ThingTracker will suffice for the pet tracker, too
    id = Column(Integer, primary_key=True)

    # link all the things to a house
    home_id = Column(Integer, ForeignKey('capstone_homes.id'), nullable=False)

    # things can be taken out of the house, so 
    room_id = Column(Integer, ForeignKey('capstone_rooms.id'))

    name = Column(Text)

class Forecast(Base):
    __tablename__ = 'capstone_forecasts'

    id = Column(Integer, primary_key=True)

    latitude = Column(Float)
    longitude = Column(Float)

    temperature = Column(Float)
    precipType = Column(Text)
    precipIntensity = Column(Float) # inches of liquid per hour
    precipProbability = Column(Float) # between 0 and 1

    time = Column(Integer)

    def __repr__(self):
        return f'<Forecast {self.time}, {self.latitude}, {self.longitude}>'

class Utilities(Base):

    # NOTE: table is only updated when usage changes
    __tablename__ = 'capstone_utilities'

    id = Column(Integer, primary_key=True)

    time = Column(Integer)
    utility_type = Column(Text)
    # usage of watts or gallons
    usage = Column(Float)

    home_id = Column(Integer, ForeignKey('capstone_homes.id'), nullable=False)

class EntryPointHistory(Base):
    # NOTE: only updated when entry points are added or removed from list

    __tablename__ = 'capstone_entry_point_history'

    id = Column(Integer, primary_key=True)

    time = Column(Integer)
    # json list of open entry points
    open_points = Column(Text)

    home_id = Column(Integer, ForeignKey('capstone_homes.id'), nullable=False)

# class PetTracker(Model):
#     id = Column(Integer, primary_key=True)

#     # link all the things to a house
#     home_id = Column(Integer, ForeignKey('home.id'), nullable=False)

#     # things can be taken out of the house, so 
#     room_id = Column(Integer, ForeignKey('room.id'))

#     name = Column(Text)

# get username config
try:
    with open('sshcfg.txt', 'r') as f:
        name = f.read()
    name = name.strip()
        # print(name.encode())
except FileNotFoundError:
    print('Create a sshcfg.txt and place your blazerid in it.')
    print('Make sure you have an ssh key made')
    exit()

# create sshtunnel
server = SSHTunnelForwarder(
    'lan.cis.uab.edu',
    ssh_username=name,
    ssh_pkey="~/.ssh/id_rsa",
    remote_bind_address=('cisdb.cis.uab.edu', 5432)
)

server.start()
local_port = server.local_bind_port

db_uri = f'postgres://smso3223web:smso3223@127.0.0.1:{local_port}/smso3223'
# db_uri = f'postgres://wjsetzer:EnLgKLzj@127.0.0.1:5432/infinitechan'
engine = create_engine(db_uri)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
