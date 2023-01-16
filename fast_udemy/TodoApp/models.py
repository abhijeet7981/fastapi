from sqlalchemy import Column,Boolean,Integer,String
from database import base

class Todo(base):
    __tablename__ = 'todos'


    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(255))
    description = Column(String(255))
    priority=Column(Integer)
    complete = Column(Boolean,default=False)





