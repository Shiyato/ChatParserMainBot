from sqlalchemy import Column, Integer, String, create_engine, func, Boolean, delete, Text
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
    type1 = Column(Integer)
    type2 = Column(Integer)
    type3 = Column(Integer)
    type4 = Column(Integer)
    type5 = Column(Integer)
    type6 = Column(Integer)
    type7 = Column(Integer)
    type8 = Column(Integer)
    type9 = Column(Integer)
    type10 = Column(Integer)

    def __repr__(self):
        return f"<User({self.id}, {self.tg_id}, {self.username}, {self.type1}, {self.type2}, {self.type3}, {self.type4}, {self.type5}, {self.type6}, {self.type7}, {self.type8}, {self.type9}, {self.type10},)>"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    tg_id = Column(String)
    username = Column(String)
    payment_id = Column(String)
    date = Column(String)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    text = Column(Text)
    contact = Column(String)
    date = Column(String)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    tg_id = Column(String)
    start_date = Column(String)
    end_date = Column(String)


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

def addPayment(tg_id:str, username:str, payment_id:str, date:str):
    payment = Payment(tg_id=tg_id, payment_id=payment_id, date=date, username=username)
    session.add(payment)
    session.commit()
    return payment

def addSubscription(tg_id:str, username:str, start_date:str, end_date:str):
    subscription = Subscription(tg_id=tg_id, start_date=start_date, end_date=end_date, username=username)
    session.add(subscription)
    session.commit()
    return subscription

def rewriteSubscription(tg_id:str, username:str, end_date):
    sub = session.query(Subscription).filter(Subscription.tg_id == tg_id).first()
    updated_rows = session.query(Subscription) \
        .filter(User.tg_id == tg_id) \
        .update({"end_date": end_date})
    session.commit()
    return updated_rows

def checkSubscription(tg_id:str):
    subscription = session.query(Subscription).filter_by(tg_id=tg_id).first()
    return subscription

def getSubscriptions():
    subscription = session.query(Subscription).all()
    return subscription

def addRequest(type:int, text:str, contact:str, date:str):
    request = Subscription(type, text, contact, date)
    session.add(request)
    session.commit()
    return request

def getUsersBySub():
    users = session.query(Subscription.tg_id).scalars().all()
    return users

def checkPayments(tg_id:str):
    payments = session.query(Payment).filter_by(tg_id=tg_id).all()
    return payments

def rewriteUser(tg_id:str, username:str, type1=None, type2=None, type3=None, type4=None, type5=None, type6=None, type7=None, type8=None, type9=None, type10=None):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    updated_rows = session.query(User) \
        .filter(User.tg_id == tg_id) \
        .update({"type1": type1 if type1 is not None else user.type1,
                 "type2": type2 if type2 is not None else user.type2,
                 "type3": type3 if type3 is not None else user.type3,
                 "type4": type4 if type4 is not None else user.type4,
                 "type5": type5 if type5 is not None else user.type5,
                 "type6": type6 if type6 is not None else user.type6,
                 "type7": type7 if type7 is not None else user.type7,
                 "type8": type8 if type8 is not None else user.type8,
                 "type9": type9 if type9 is not None else user.type9,
                 "type10": type10 if type10 is not None else user.type10
                 })
    session.commit()
    return updated_rows

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

def getUsersByCat(key:int):
    if key == 1:
        user = session.query(User).filter(User.type1 != None, User.type1 != '').all()
    elif key == 2:
        user = session.query(User).filter(User.type2 != None, User.type2 != '').all()
    elif key == 3:
        user = session.query(User).filter(User.type3 != None, User.type3 != '').all()
    elif key == 4:
        user = session.query(User).filter(User.type4 != None, User.type4 != '').all()
    elif key == 5:
        user = session.query(User).filter(User.type5 != None, User.type5 != '').all()
    elif key == 6:
        user = session.query(User).filter(User.type6 != None, User.type6 != '').all()
    elif key == 7:
        user = session.query(User).filter(User.type7 != None, User.type7 != '').all()
    elif key == 8:
        user = session.query(User).filter(User.type8 != None, User.type8 != '').all()
    elif key == 9:
        user = session.query(User).filter(User.type9 != None, User.type9 != '').all()
    elif key == 10:
        user = session.query(User).filter(User.type10 != None, User.type10 != '').all()
    return user

def getUsersIdByCat(key:int):
    if key == 1:
        user = session.query(User.id).filter(User.type1 != None, User.type1 != '').scalars().all()
    elif key == 2:
        user = session.query(User.id).filter(User.type2 != None, User.type2 != '').scalars().all()
    elif key == 3:
        user = session.query(User.id).filter(User.type3 != None, User.type3 != '').scalars().all()
    elif key == 4:
        user = session.query(User.id).filter(User.type4 != None, User.type4 != '').scalars().all()
    elif key == 5:
        user = session.query(User.id).filter(User.type5 != None, User.type5 != '').scalars().all()
    elif key == 6:
        user = session.query(User.id).filter(User.type6 != None, User.type6 != '').scalars().all()
    elif key == 7:
        user = session.query(User.id).filter(User.type7 != None, User.type7 != '').scalars().all()
    elif key == 8:
        user = session.query(User.id).filter(User.type8 != None, User.type8 != '').scalars().all()
    elif key == 9:
        user = session.query(User.id).filter(User.type9 != None, User.type9 != '').scalars().all()
    elif key == 10:
        user = session.query(User.id).filter(User.type10 != None, User.type10 != '').scalars().all()
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