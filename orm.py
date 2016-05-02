#!/usr/bin/env python

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import *
from sqlalchemy import orm

def connect():
    return psycopg2.connect("dbname=m4 user=sami")
engine = create_engine('postgresql+psycopg2://', creator=connect) #connect to the database server
Base = declarative_base()
Session = sessionmaker(bind=engine)	#create the session mapper
session = Session() #initialize the session


# Perform the mapping with classes and database tables
meta = MetaData()
meta.reflect(bind=engine)

class Clients(object):
	pass
class theTables(object):
	pass
class Payements(object):
	pass
class Orders(object):
	pass
class Drinks(object):
	pass
class OrderedDrinks(object):
	pass

orm.Mapper(Clients, meta.tables['clients'])
orm.Mapper(theTables, meta.tables['thetables'])
orm.Mapper(Payements, meta.tables['payements'])
orm.Mapper(Orders, meta.tables['orders'])
orm.Mapper(Drinks, meta.tables['drinks'])
orm.Mapper(OrderedDrinks, meta.tables['ordereddrinks'])

'''	
Clients = meta.tables['clients']
theTables = meta.tables['thetables']
Payements = meta.tables['payements']
Orders = meta.tables['orders']
Drinks = meta.tables['drinks']
OrderedDrinks = meta.tables['ordereddrinks']
'''

'''
print session.query(Clients).all()
print session.query(theTables).all()
print session.query(Payements).all()
print session.query(Orders).all()
print session.query(Drinks).all()
print session.query(OrderedDrinks).all()
'''

'''
All classes used for the mapping
'''

'''
class Clients(Base):
	__tablename__ = 'clients'
	tokenNumber = Column(Integer, primary_key=True, autoincrement=True)
	amountDue = Column(Integer)
	order = relationship("Orders", back_populates="client")
	def __repr__(self):
		return "<Clients(tokenNumber='%i', amountDue='%i')>" % (self.tokenNumber, self.amountDue)

class theTables(Base):
	__tablename__ = 'theTables'
	tableNumber = Column(Integer, primary_key=True)
	codebar = Column(Integer)
	isFree = Column(Boolean)
	tokenNumber = Column(Integer)
	def __repr__(self):
		return "<theTables(tableNumber='%i', codebar='%i', isFree='%r', tokenNumber='%i')>" % (self.tableNumber, self.codebar, self.isFree, self.tokenNumber)

class Payements(Base):
	__tablename__ = 'Payements'
	payementNumber = Column(Integer, primary_key=True)
	amountPayed = Column(Integer)
	def __repr__(self):
		return "<Payements(payementNumber='%i', amountPayed='%i')>" % (self.payementNumber, self.amountPayed)

class Orders(Base):
	__tablename__ = 'Orders'
	orderNumber = Column(Integer, primary_key=True)
	orderTime = Column(DateTime)
	tokenNumber = Column(Integer, ForeignKey('Clients.tokenNumber'))
	client = relationship("Clients", back_populates="order")

	def __repr__(self):
		return "<Orders(orderNumber='%i', orderTime='%s', tokenNumber='%i')>" % (self.orderNumber, self.orderTime, self.tokenNumber)

class Drinks(Base):
	__tablename__ = 'Drinks'
	drinkNumber = Column(Integer, primary_key=True)
	price = Column(Integer)
	name = Column(String)
	description = Column(String)
	def __repr__(self):
		return "<Drinks(drinkNumber='%i', price='%i', name='%s', description='%s')>" % (self.drinkNumber, self.price, self.name, self.description)

class OrderedDrinks(Base):
	__tablename__ = 'OrderedDrinks'
	orderedNumber = Column(Integer, ForeignKey('Orders.orderNumber'), primary_key=True)
	drinkNumber = Column(Integer, ForeignKey('Drinks.drinkNumber'), primary_key=True)
	qty = Column(Integer)
	#ForeignKeyConstraint(['orderedNumber', 'drinkNumber'], ['Orders.orderNumber', 'Drinks.drinkNumber'])
	def __repr__(self):
		return "<OrderedDrinks(orderedNumber='%i', drinkNumber='%i', qty='%i')>" % (self.orderedNumber, self.drinkNumber, self.qty)
'''
#Base.metadata.create_all(engine) #Create the tables

def populate():
	#delete everythings
	q = [session.query(Clients).all(), session.query(theTables).all(), session.query(Payements).all(), session.query(Orders).all(), session.query(Drinks).all(), session.query(OrderedDrinks).all()]
	for t in q:
		for e in t:
			session.delete(e)
	session.commit()

	# Add 3 clients
	client1 = Clients(amountDue=14, tokenNumber=1)
	client2 = Clients(amountDue=7, tokenNumber=2)
	client3 = Clients(amountDue=21, tokenNumber=3)
	session.add(client1)
	session.add(client2)
	session.add(client3)
	session.commit()

	# Add 5 tables
	tables1 = theTables(tableNumber=1, codebar=10, isFree=False, tokenNumber=1)
	tables2 = theTables(tableNumber=2, codebar=20, isFree=True, tokenNumber=1)
	tables3 = theTables(tableNumber=3, codebar=30, isFree=False, tokenNumber=2)
	tables4 = theTables(tableNumber=4, codebar=40, isFree=False, tokenNumber=3)
	tables5 = theTables(tableNumber=5, codebar=50, isFree=True, tokenNumber=2)
	session.add(tables1)
	session.add(tables2)
	session.add(tables3)
	session.add(tables4)
	session.add(tables5)
	session.commit()
	  
	# Add 4 orders
	order1 = Orders(orderTime='2016-04-28 12:59:01', tokenNumber=1, orderNumber=1)
	order2 = Orders(orderTime='2016-04-28 13:10:22', tokenNumber=2, orderNumber=2)
	order3 = Orders(orderTime='2016-04-28 13:30:53', tokenNumber=3, orderNumber=3)
	order4 = Orders(orderTime='2016-04-28 13:58:47', tokenNumber=3, orderNumber=4)
	session.add(order1)
	session.add(order2)
	session.add(order3)
	session.add(order4)
	session.commit()

	# Add 4 Drinks
	drink1 = Drinks(drinkNumber=1, price=1, name='Water', description='Non sparkling water')
	drink2 = Drinks(drinkNumber=2, price=2, name='Sparkling water', description='A marvellous sparling water')
	drink3 = Drinks(drinkNumber=3, price=2, name='Fanta', description='An orange fanta')
	drink4 = Drinks(drinkNumber=4, price=2, name='Cafe', description='A good old black cafe')
	session.add(drink1)
	session.add(drink2)
	session.add(drink3)
	session.add(drink4)
	session.commit()

	# Add 5 orderedDrinks
	orderedDrinks1 = OrderedDrinks(orderedNumber=1, drinkNumber=2, qty=3)
	orderedDrinks2 = OrderedDrinks(orderedNumber=2, drinkNumber=1, qty=4)
	orderedDrinks3 = OrderedDrinks(orderedNumber=3, drinkNumber=4, qty=1)
	orderedDrinks4 = OrderedDrinks(orderedNumber=4, drinkNumber=2, qty=2)
	orderedDrinks5 = OrderedDrinks(orderedNumber=4, drinkNumber=3, qty=6)
	session.add(orderedDrinks1)
	session.add(orderedDrinks2)
	session.add(orderedDrinks3)
	session.add(orderedDrinks4)
	session.add(orderedDrinks5)
	session.commit()

	# Add 3 payements
	payement1 = Payements(amountPayed=8)
	payement2 = Payements(amountPayed=80)
	payement3 = Payements(amountPayed=24)
	session.add(payement1)
	session.add(payement2)
	session.add(payement3)
	session.commit()

#populate()


#
#	FUNCTIONS
#

'''AcquireTable
 * DESC: invoked by the smartphone app when scanning a table code bar.
 * IN:  a table bar code.
 * OUT: a client token.
 * PRE: the table is free.
 * POST: the table is no longer free.
 * POST: issued token can be used for ordering drinks.
 '''
def AcquireTable(tableCodebar):
	#tabletest = session.query(theTables).first().codebar
	#print tabletest
	table = session.query(theTables).filter(theTables.codebar == tableCodebar).first()
	if (table is None):
		raise NameError('The table is not available or not existing.')
	
	# create new client
	newClient = Clients()
	newClient.amountdue = 0
	session.add(newClient)
	session.commit()

	# update the table so that it is no longer free
	table.isfree = False
	table.tokennumber = newClient.tokennumber
	session.add(table)
	session.commit()

	# return the coyrrent value of tokenNumber (last client created)
	session.refresh(newClient)
	return newClient.tokennumber

# Function verifying that the client token is valid and corresponds to an occupied table.
def checkTable(token):
	theTable = session.query(theTables).filter(and_(theTables.tokennumber == token, theTables.isfree == False)).first()
	if (theTable is None):
		raise NameError('The client token is not valid or does not correspond to an occupied table.')
	return theTable

'''OrderDrinks 
 * DESC:  invoked when the user presses the "order" button in the ordering screen.
 * IN: a client token.
 * IN: a list of (drink, qty) taken from the screen form.
 * OUT: the unique number of the created order.
 * PRE: the client token is valid and corresponds to an occupied table.
 * POST: the order is created, its number is the one returned.
 '''
def OrderDrinks(token, drinkList):
	theTable = checkTable(token)
	order = Orders()
	order.ordertime = func.now()
	order.tokennumber = token
	session.add(order)
	session.commit()
	session.refresh(order)
	theOrder = order.ordernumber

	amount = 0
	for anOrderedDrink in drinkList:
		anAmount = session.query(Drinks).filter(Drinks.drinknumber == anOrderedDrink[0]).first().price
		amount += anAmount * anOrderedDrink[1]

		ordereddrink = OrderedDrinks()
		ordereddrink.ordernumber = theOrder
		ordereddrink.drinknumber = anOrderedDrink[0]
		ordereddrink.qty = anOrderedDrink[1]
		session.add(ordereddrink)
		session.commit()

	client = session.query(Clients).filter(Clients.tokennumber == token).first()
	client.amountdue += amount
	session.commit()

	return theOrder

'''IssueTicket 
 * DESC: invoked when the user asks for looking at the table summary and due amount.
 * IN: a client token.
 * OUT: the ticket to be paid, with a summary of orders (which drinks in which quantities) and total amount to pay.
 * PRE: the client token is valid and corresponds to an occupied table.
 * POST: issued ticket corresponds to all (and only) ordered drinks at that table.
 ''' 
def IssueTicket(token):
	theTable = checkTable(token)
	amount = session.query(Clients).filter(Clients.tokennumber == token).first().amountdue
	orders = session.query(Orders).filter(Orders.tokennumber == token).all()
	orderList = []
	for o in orders:
		orderList += [o.ordernumber]
	#orderedDrinkList = session.query(OrderedDrinks).filter(OrderedDrinks.ordernumber in orderList).first()
	orderedDrinks = session.query(OrderedDrinks).all()
	orderedDrinkList = []
	for o in orderedDrinks:
		if(o.ordernumber in orderList):
			orderedDrinkList += [o.ordernumber]
	return [amount, orderedDrinkList]


'''PayTable 
 * DESC:  invoked by the smartphone on confirmation from the payment gateway (we ignore security on purpose here; a real app would never expose such an API, of course).
 * IN: a client token.
 * IN:  an amount paid.
 * OUT:
 * PRE: the client token is valid and corresponds to an occupied table.
 * PRE: the input amount is greater or equal to the amount due for that table.
 * POST: the table is released.
 * POST: the client token can no longer be used for ordering
 '''
def PayTable(token, amount):
 	#We start by verifying the preconditions.
 	theTable = checkTable(token);
 	theAmountDue = session.query(Clients).filter(Clients.tokennumber == token).first().amountdue
 	if(amount < theAmountDue):
 		raise NameError('The amount payed is not enough to pay what is due.')
 	else:
 		payement = Payements()
 		payement.amountPayed = amount
 		session.commit()

 	#The client token will non longer be used for ordering.
 	client = session.query(Clients).filter(Clients.tokennumber == token).first()
 	session.delete(client)

 	#We update the table, because it is now free.
 	table = session.query(theTables).filter(theTables.tokennumber == token).first()
	table.isfree = True
	session.add(table)
	session.commit()


''' INSERT
client1 = Client(tokennumber=3, amountdue=25)
session.add(client1)
session.commit()
'''

''' Query with filter
client1 = session.query(Clients).filter(Clients.amountDue == 25).all()
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


#
# Sparkling Water Script
#
def sparkling_script():

	#The client acquire the second table and we get the client token.
	#q1 = SELECT INTO client AcquireTable(20);
	client = AcquireTable(20)

	# The client orders a sparkling water.
	#q2 = SELECT INTO firstOrder OrderDrinks(client,ARRAY[[2,1]]);
	orderSparkling = [[1,2]]
	firstOrder = OrderDrinks(client, orderSparkling)

	# The client then looks at his bill.
	#q3 = SELECT INTO ticket IssueTicket(client);
	ticket = IssueTicket(client)

	# The client then order another sparkling water.
	#q4 = SELECT INTO secondOrder OrderDrinks(client,ARRAY[[2,1]]);
	secondOrder = OrderDrinks(client, orderSparkling)

	# Finally, the client pays and release the table.
	#q5 = SELECT INTO tablePaid PayTable(client,4);
	#tablePaid = PayTable(client, 4)

sparkling_script()