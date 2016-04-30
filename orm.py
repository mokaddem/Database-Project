#!/usr/bin/env python

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


def connect():
    return psycopg2.connect("dbname=m4 user=sami")
engine = create_engine('postgresql+psycopg2://', creator=connect) #connect to the database server
Base = declarative_base()
Session = sessionmaker(bind=engine)	#create the session mapper
session = Session() #initialize the session

'''
All classes used for the mapping
'''
class Clients(Base):
	__tablename__ = 'Clients'
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
	#relationship("Child", backref=backref("parent", uselist=False))

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

Base.metadata.create_all(engine) #Create the mapping

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

#
#	FUNCTIONS
#

'''
 * AcquireTable
 * DESC: invoked by the smartphone app when scanning a table code bar.
 * IN:  a table bar code.
 * OUT: a client token.
 * PRE: the table is free.
 * POST: the table is no longer free.
 * POST: issued token can be used for ordering drinks.
'''
def AcquireTable(tableCodebar):
	if (session.query(theTables).filter(theTables.codebar == tableCodebar).first() is None):
		raise NameError('The table is not available or not existing.')
	
	# create new client
	newClient = Clients(amountDue=0)
	session.add(newClient)
	session.commit()

	# update the table so that it is no longer free
	table = session.query(theTables).filter(theTables.codebar == tableCodebar).first()
	table.isFree = False
	session.add(table)
	session.commit()

	# return the coyrrent value of tokenNumber (last client created)
	session.refresh(newClient)
	return newClient.tokenNumber

# Function verifying that the client token is valid and corresponds to an occupied table.
def checkTable(token):
	theTable = session.query(theTables).filter(and_(theTables.tokenNumber == token, theTables.isFree == False)).first()
	if (theTable is None):
		raise NameError('The client token is not valid or does not correspond to an occupied table.')
	return theTable

'''
 * OrderDrinks 
 * DESC:  invoked when the user presses the “order” button in the ordering screen.
 * IN: a client token.
 * IN: a list of (drink, qty) taken from the screen form.
 * OUT: the unique number of the created order.
 * PRE: the client token is valid and corresponds to an occupied table.
 * POST: the order is created, its number is the one returned.
 '''
def OrderDrinks(token, drinkList):

  -- NOTE: the second argument is not a list of (drink,qty) but a list of integer such that (drink1,qty1,drink2,qty2,...).
CREATE OR REPLACE FUNCTION OrderDrinks(token integer, drinkList integer[]) RETURNS integer AS $$
    DECLARE
      anOrderedDrink integer[];
      theTable integer;
      amount integer;
      anAmount integer;
      theOrder integer;
    BEGIN
      -- We start by verifying the preconditions.
      theTable = checkTable(token);

      -- We then insert the order into Orders.
      INSERT INTO Orders (orderTime,tokenNumber) VALUES (now(),token) RETURNING orderNumber INTO theOrder;

      -- And all the orderedDrinks into OrderedDrinks, while computing the amount due.
      amount := 0;
      FOREACH anOrderedDrink SLICE 1 IN ARRAY drinkList LOOP
        SELECT INTO anAmount price FROM Drinks WHERE anOrderedDrink[1] = drinkNumber;
	amount := amount + anAmount*anOrderedDrink[2];
	INSERT INTO OrderedDrinks (orderNumber, drinkNumber, qty) VALUES (theOrder, anOrderedDrink[1], anOrderedDrink[2]);
      END LOOP;
      
      -- We add the amount to the one already due by the client.
      UPDATE Clients SET amountDue = amountDue + amount WHERE tokenNumber = token;
      
      RETURN theOrder;
    END;
    $$LANGUAGE plpgsql;


























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

#populate()