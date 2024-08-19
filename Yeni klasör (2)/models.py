from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Employee(Base):
 __tablename__= 'employees'
   
 id= Column(Integer, primary_key=True,index=True)
 username= Column(String(50),unique=True)
 mail=Column(String(50),unique=True)


class Post(Base):
 __tablename__ = 'posts'

 id=Column(Integer, primary_key=True, index=True)
 title= Column(String(50))
 content= Column(String(50))
 employee_id=Column(Integer)