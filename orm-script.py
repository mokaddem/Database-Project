/*
 * This script execute the "sparkling water" example.
 */

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

def connect():
  return psycopg2.connect("dbname=m4 user=sami")
engine = create_engine('postgresql+psycopg2://', creator=connect) #connect to the database server
Base = declarative_base()
Session = sessionmaker(bind=engine) #create the session mapper
session = Session() #initialize the session

#The client acquire the second table and we get the client token.
session.callproc('AcquireTable', [20])
client = list(session.fetchall())

#The client orders a sparkling water.
session.callproc('OrderDrinks', [client, [[2,1]] ])
firstOrder = list(session.fetchall())

#The client then looks at his bill.
session.callproc('IssueTicket', [client])
ticket = list(session.fetchall())

#The client then order another sparkling water.
session.callproc('OrderDrinks', [client, [[2,1]] ])
secondOrder = list(session.fetchall())

#Finally, the client pays and release the table.
session.callproc('PayTable', [client, 4])
tablePaid = list(session.fetchall())
