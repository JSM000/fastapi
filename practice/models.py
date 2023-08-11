from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

    # primary_key
    # nullable = False
    # unique
    # autoincrement
    # default

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    code = Column(String(100), unique=True)
    area_code = Column(String(100))
    name = Column(String(100))

    user = relationship("User", back_populates="school")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    email = Column(String(100), unique=True)
    social_id = Column(String(100), nullable= True, unique=True)
    password = Column(String(100))
    nickname = Column(String(100), nullable= True, unique=True)
    birthday = Column(Integer, nullable= True)
    last_login = Column(Integer, nullable= True)
    joined_at = Column(Integer, nullable= True)
    avartar_sgv = Column(String(100), nullable= True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_male = Column(Boolean, nullable= True)

    school_id =  Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="user")
    student = relationship("Student", back_populates="user")



class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    num = Column(Integer)
    name = Column(String(100))
    ismale = Column(Boolean)
    
    user_id =  Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="student")