#!/usr/bin/env python

import psycopg2

# Connect to the database
conn = psycopg2.connect("dbname=m4 user=sami")

# Open a cursor to perform database operations
cur = conn.cursor()


#The client acquire the second table and we get the client token.
#q1 = SELECT INTO client AcquireTable(20);
cur.callproc('AcquireTable', [20, ])
client = cur.fetchone()

# The client orders a sparkling water.
#q2 = SELECT INTO firstOrder OrderDrinks(client,ARRAY[[2,1]]);
orderSparkling = [[1,2]]
cur.callproc('OrderDrinks', [client, orderSparkling,])
firstOrder = cur.fetchone()

# The client then looks at his bill.
#q3 = SELECT INTO ticket IssueTicket(client);
cur.callproc('IssueTicket', [client,])
ticket = cur.fetchone()

# The client then order another sparkling water.
#q4 = SELECT INTO secondOrder OrderDrinks(client,ARRAY[[2,1]]);
cur.callproc('OrderDrinks', [client, orderSparkling,])
secondOrder = cur.fetchone()

# Finally, the client pays and release the table.
#q5 = SELECT INTO tablePaid PayTable(client,4);
cur.callproc('PayTable', [client, 4,])
tablePaid = cur.fetchone()
