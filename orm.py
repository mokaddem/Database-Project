#!/usr/bin/env python

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from sqlalchemy.orm import sessionmaker


def connect():
    return psycopg2.connect("dbname=m4 user=sami")
engine = create_engine('postgresql+psycopg2://', creator=connect) #connect to the database server
Base = declarative_base()
Session = sessionmaker(bind=engine)	#create the session mapper
session = Session() #initialize the session

'''
All classes used for the mapping
'''
class Client(Base):
	__tablename__ = 'client'
	tokennumber = Column(Integer, primary_key=True)
	amountdue = Column(Integer)
	def __repr__(self):
		return "<client(tokennumber='%i', amountdue='%i')>" % (self.tokennumber, self.amountdue)

class Table(Base):
	__tablename__ = 'thetable'
	tablenumber = Column(Integer, primary_key=True)
	codebar = Column(Integer)
	isFree = Column(Boolean)
	def __repr__(self):
		return "<table(tablenumber='%i', codebar='%i', isFree='%b')>" % (self.tablenumber, self.codebar, self.isFree)

class Payement(Base):
	__tablename__ = 'payement'
	payementnumber = Column(Integer, primary_key=True)
	amountpaid = Column(Integer)
	def __repr__(self):
		return "<payement(payementnumber='%i', amountpaid='%i')>" % (self.payementnumber, self.amountpaid)

class Orders(Base):
	__tablename__ = 'orders'
	ordernumber = Column(Integer, primary_key=True)
	ordertime = Column(DateTime)
	def __repr__(self):
		return "<orders(ordernumber='%i', ordertime='%s')>" % (self.ordernumber, self.ordertime)

class Drink(Base):
	__tablename__ = 'drink'
	tokennumber = Column(Integer, primary_key=True)
	price = Column(Integer)
	name = Column(String)
	description = Column(String)
	def __repr__(self):
		return "<drink(tokennumber='%i', price='%i', name='%s', description='%s')>" % (self.tokennumber, self.price, self.name, self.description)

class OrderedDrink(Base):
	__tablename__ = 'OrderedDrink'
	orderednumber = Column(Integer, primary_key=True)
	drinknumber = Column(Integer)
	qty = Column(Integer)
	def __repr__(self):
		return "<OrderedDrink(orderednumber='%i', drinknumber='%i', qty='%i')>" % (self.orderednumber, self.drinknumber, self.qty)


Base.metadata.create_all(engine) #Create the mapping



''' INSERT
client1 = Client(tokennumber=3, amountdue=25)
session.add(client1)
session.commit()
'''

''' Query with filter
client1 = session.query(Client).filter(Client.amountdue == 25).all()
print client1
'''


''' Update value
client1 = session.query(Client).filter(Client.amountdue == 25).first()
client1.amountdue = 35
session.add(client1)
session.commit()
'''

''' Delete value
client1 = = session.query(Client).filter(Client.amountdue == 25).first()
session.delete(client1)
session.commit()
'''







#session.query(Client).filter_by(tokennumber==1).first()