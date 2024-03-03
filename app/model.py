from sqlalchemy import Column, Integer, String, Boolean
from config import Base
from datetime import datetime


class Profile(Base):
    __tablename__ = 'profile'

    id= Column(Integer, primary_key=True)
    reference = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    other_name = Column(String)
    gender = Column(String)
    birthday = Column(String)
    organization_id = Column(Integer)
    email = Column(String)
    password = Column(String)
    phone_number = Column(Integer)
    display_image = Column(String)
    bio = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    profile_id = Column(Integer)
    login_status = Column(Boolean, default=False)  # Default value set to False
    status = Column(String, default="pending")
    enabled = Column(Boolean, default=False)  # Default value set to False

