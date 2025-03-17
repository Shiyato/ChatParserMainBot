from sqlalchemy import Column, Integer, String, create_engine, func, Boolean, delete
from sqlalchemy.orm import declarative_base, sessionmaker
import random, config
import pandas as pd

engine = create_engine('sqlite:///db.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(String)
    username = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    type3 = Column(String)
    type4 = Column(String)
    type5 = Column(String)
    type6 = Column(String)
    type7 = Column(String)
    type8 = Column(String)
    type9 = Column(String)
    type10 = Column(String)

    def __repr__(self):
        return f"<User({self.id}, {self.tg_id}, {self.username}, {self.type1}, {self.type2}, {self.type3}, {self.type4}, {self.type5}, {self.type6}, {self.type7}, {self.type8}, {self.type9}, {self.type10},)>"

def dbCreate():
    Base.metadata.create_all(bind=engine)

def dbRenew():
    Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(bind=engine)

def addUser(tg_id:str, username:str, type1=0, type2=0, type3=0, type4=0, type5=0, type6=0, type7=0, type8=0, type9=0, type10=0):
    user = User(tg_id=tg_id, username=username, type1=type1, type2=type2, type3=type3, type4=type4, type5=type5, type6=type6, type7=type7, type8=type8, type9=type9, type10=type10)
    session.add(user)
    session.commit()
    return user


def rewriteUser(tg_id:str, username:str, type1=0, type2=0, type3=0, type4=0, type5=0, type6=0, type7=0, type8=0, type9=0, type10=0):
    user = getUserByTgID(tg_id)
    user.type1 = type1 if type1 else user.type1
    user.type2 = type2 if type2 else user.type2
    user.type3 = type3 if type3 else user.type3
    user.type4 = type4 if type4 else user.type4
    user.type5 = type5 if type5 else user.type5
    user.type6 = type6 if type6 else user.type6
    user.type7 = type7 if type7 else user.type7
    user.type8 = type8 if type8 else user.type8
    user.type9 = type9 if type9 else user.type9
    user.type10 = type10 if type10 else user.type10
    session.commit()
    return user

def getUserByID(key:int):
    user = session.query(User).get(key)
    return user

def getAllUsers():
    user = session.query(User).all()
    return user

def getUserByTgID(key:str):
    user = session.query(User).filter_by(tg_id=key).first()
    return user

def getUserByUsername(key:str):
    user = session.query(User).filter_by(username=key).first()
    return user

def getUsersBySub(key:int):
    if key == 1:
        user = session.query(User).filter(User.type1 != None, User.type1 != '')
    elif key == 2:
        user = session.query(User).filter(User.type2 != None, User.type2 != '')
    elif key == 3:
        user = session.query(User).filter(User.type3 != None, User.type3 != '')
    elif key == 4:
        user = session.query(User).filter(User.type4 != None, User.type4 != '')
    elif key == 5:
        user = session.query(User).filter(User.type5 != None, User.type5 != '')
    elif key == 6:
        user = session.query(User).filter(User.type6 != None, User.type6 != '')
    elif key == 7:
        user = session.query(User).filter(User.type7 != None, User.type7 != '')
    elif key == 8:
        user = session.query(User).filter(User.type8 != None, User.type8 != '')
    elif key == 9:
        user = session.query(User).filter(User.type9 != None, User.type9 != '')
    elif key == 10:
        user = session.query(User).filter(User.type10 != None, User.type10 != '')
    return user

def checkUsers():
    import sqlite3
    conn = sqlite3.connect('db.db')
    query = "SELECT * FROM users"
    data_frame = pd.read_sql(query, conn)
    print(data_frame.head())

def exportDB():
    import sqlite3
    conn = sqlite3.connect('db.db')

    query = "SELECT * FROM users"
    data_frame = pd.read_sql(query, conn)
    excel_file_path = 'users.xlsx'
    data_frame.to_excel(excel_file_path, index=False)

    query = "SELECT * FROM meets"
    data_frame = pd.read_sql(query, conn)
    excel_file_path = 'meets.xlsx'
    data_frame.to_excel(excel_file_path, index=False)

    query = "SELECT * FROM codes"
    data_frame = pd.read_sql(query, conn)
    excel_file_path = 'codes.xlsx'
    data_frame.to_excel(excel_file_path, index=False)