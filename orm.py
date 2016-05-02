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

#
# Perform the mapping with classes and database tables
#
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
	orderedDrinks = session.query(OrderedDrinks).all()
	orderedDrinkList = []
	for o in orderedDrinks:
		if(o.ordernumber in orderList):
			orderedDrinkList += [(o.drinknumber, o.qty)]
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

#
# Sparkling Water Script
#
def sparkling_script():

	#The client acquire the second table and we get the client token.
	client = AcquireTable(20)
	#print client

	# The client orders a sparkling water.
	orderSparkling = [[2,1]]
	firstOrder = OrderDrinks(client, orderSparkling)
	#print firstOrder

	# The client then looks at his bill.
	ticket = IssueTicket(client)
	#print ticket

	# The client then order another sparkling water.
	secondOrder = OrderDrinks(client, orderSparkling)
	#print secondOrder

	ticket = IssueTicket(client)
	#print ticket

	# Finally, the client pays and release the table.
	tablePaid = PayTable(client, 4)

sparkling_script()