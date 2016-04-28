
/*
 *  We generate the 6 needed tables. If they existed before, they are dropped.
 */
DROP TABLE IF EXISTS Clients CASCADE;
DROP TABLE IF EXISTS theTables CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Drinks CASCADE;
DROP TABLE IF EXISTS OrderedDrinks CASCADE;
DROP TABLE IF EXISTS Payements CASCADE;

CREATE TABLE Clients (
  tokenNumber SERIAL primary key,
  amountDue integer
);

CREATE TABLE theTables (
  tableNumber integer primary key,
  codebar integer,
  isFree boolean,
  tokenNumber integer
  --foreign key (tokenNumber) references Clients (tokenNumber)
  --We can't do that, or we won't be able to delete the clients that have payed.
);

CREATE TABLE Orders (
  orderNumber SERIAL primary key,
  orderTime timestamp,
  tokenNumber integer
  --foreign key (tokenNumber) references Clients (tokenNumber)
  -- We won't be needing that thanks to the cascading delete.
);

CREATE TABLE Drinks (
  drinkNumber integer primary key,
  price integer,
  name varchar(20),
  description varchar(100)
);

CREATE TABLE OrderedDrinks (
  orderNumber integer,
  drinkNumber integer,
  qty integer,
  primary key (orderNumber, drinkNumber),
  foreign key (orderNumber) references Orders (orderNumber),
  foreign key (drinkNumber) references Drinks (drinkNumber)
);

CREATE TABLE Payements (
  payementNumber SERIAL primary key,
  amountPayed integer
);

/*
 *  Now we populate the database. If any value existed, it is deleted before.
 */
DELETE FROM Clients;
DELETE FROM theTables;
DELETE FROM Orders;
DELETE FROM Drinks;
DELETE FROM OrderedDrinks;
DELETE FROM Payements;

INSERT INTO Clients (amountDue) VALUES
  (14),
  (7),
  (21);

INSERT INTO theTables (tableNumber, codebar, isFree, tokenNumber) VALUES
  (1, 10, false, 1),
  (2, 20, true, 1), -- An unoccupied table remembers the tokenNumber of the last client on it.
  (3, 30, false, 2),
  (4, 40, false, 3),
  (5, 50, true, 2);
  

INSERT INTO Orders (orderTime, tokenNumber) VALUES
  ('2016-04-28 12:59:01', 1),
  ('2016-04-28 13:10:22', 2),
  ('2016-04-28 13:30:53', 3),
  ('2016-04-28 13:58:47', 3);

INSERT INTO Drinks (drinkNumber, price, name, description) VALUES
  (1, 1, 'Water', 'Non sparkling water'),
  (2, 2, 'Sparkling water', 'A marvellous sparling water'),
  (3, 2, 'Fanta', 'An orange fanta'),
  (4, 2, 'Cafe', 'A good old black cafe');

INSERT INTO OrderedDrinks (orderNumber, drinkNumber, qty) VALUES
  (1, 2, 3),
  (2, 1, 4),
  (3, 4, 1),
  (4, 2, 2),
  (4, 3, 6);

INSERT INTO Payements (amountPayed) VALUES
  (8),
  (80),
  (24);

/*
 * 3: we generate the 4 required procedure.
 */

/*
 * AcquireTable
 * DESC: invoked by the smartphone app when scanning a table code bar.
 * IN:  a table bar code.
 * OUT: a client token.
 * PRE: the table is free.
 * POST: the table is no longer free.
 * POST: issued token can be used for ordering drinks.
 */
CREATE OR REPLACE FUNCTION AcquireTable(tableCodebar integer) RETURNS integer AS $$
  DECLARE
    theTable RECORD;
    token integer;
  BEGIN
    -- We start by verifying that the table is free (and exists).
    SELECT INTO theTable * FROM theTables WHERE codebar = tableCodebar AND isFree = true;
    IF NOT FOUND THEN
	RAISE EXCEPTION 'The table % is not available or not existing.', tableCodebar;
    END IF;

    -- We update the table, because it is no longer free.
    UPDATE theTables SET isFree = false WHERE codebar = tableCodebar;
    
    -- We create the new clients, so that his (new) token can be used for ordering drinks.
    INSERT INTO Clients (amountDue) VALUES (0) RETURNING tokenNumber INTO token;
	
    -- We return the current value of tokenNumber, that is, the one of the last client created.
    RETURN token;
  END;
  $$LANGUAGE plpgsql;


/*
 * Function verifying that the client token is valid and corresponds to an occupied table.
 */
CREATE OR REPLACE FUNCTION checkTable(token integer) RETURNS integer AS $$
    DECLARE
      theTable integer;
    BEGIN
      SELECT INTO theTable * FROM theTables WHERE token = tokenNumber AND isFree = false;
      IF NOT FOUND THEN
	RAISE EXCEPTION 'The client token % is not valid or does not correspond to an occupied table.', token;
      END IF;
      RETURN theTable;
    END;
    $$LANGUAGE plpgsql;

/*
 * OrderDrinks 
 * DESC:  invoked when the user presses the “order” button in the ordering screen.
 * IN: a client token.
 * IN: a list of (drink, qty) taken from the screen form.
 * OUT: the unique number of the created order.
 * PRE: the client token is valid and corresponds to an occupied table.
 * POST: the order is created, its number is the one returned.
 */
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
        SELECT INTO anAmount price*qty FROM Drinks WHERE anOrderedDrink[1] = drinkNumber;
	amount := amount + anAmount;
	INSERT INTO OrderedDrinks (orderNumber, drinkNumber, qty) VALUES (theOrder, anOrderedDrink[1], anOrderedDrink[2]);
      END LOOP;
      
      -- We add the amount to the one already due by the client.
      UPDATE Clients SET amountDue = amountDue + amount WHERE tokenNumber = token;
      
      RETURN theOrder;
    END;
    $$LANGUAGE plpgsql;

/*
SELECT OrderDrinks(3,ARRAY[[2,5],[3,2]]);
SELECT * FROM Orders;
SELECT * FROM OrderedDrinks;
*/
    
/*
 * IssueTicket 
 * DESC: invoked when the user asks for looking at the table summary and due amount.
 * IN: a client token.
 * OUT: the ticket to be paid, with a summary of orders (which drinks in which quantities) and total amount to pay.
 * PRE: the client token is valid and corresponds to an occupied table.
 * POST: issued ticket corresponds to all (and only) ordered drinks at that table.
 */ 
CREATE OR REPLACE FUNCTION IssueTicket(token integer) RETURNS RECORD AS $$
    DECLARE
      theTable integer;
      amount integer;
      orderList RECORD;
      orderedDrinkList varchar(10)[];
    BEGIN
      -- We start by verifying the preconditions.
      theTable = checkTable(token);

      -- Find the amount due.
      SELECT INTO amount amountDue FROM Clients WHERE tokenNumber = token;

      -- SELECT INTO orderList orderNumber FROM Orders WHERE token = Orders.tokenNumber
      -- Why isn't this working?
      -- What's more, this is utterly stupid: see if we can do anything in tuple.
      orderedDrinkList := array(SELECT (drinkNumber,qty) FROM OrderedDrinks WHERE OrderedDrinks.orderNumber IN (SELECT orderNumber FROM Orders WHERE token = Orders.tokenNumber));
      
      RETURN (amount,orderedDrinkList);
    END;
    $$LANGUAGE plpgsql;

--SELECT IssueTicket(3);

/*
 * The procedure used when we are deleting a client.
 * Deletes everything related to the client.
 */
CREATE OR REPLACE FUNCTION DeleteClient() RETURNS TRIGGER AS $$
    BEGIN
      DELETE FROM Orders WHERE tokenNumber = OLD.tokenNumber;
      RETURN NULL;
    END;
    $$LANGUAGE plpgsql;
    
/*
 * The trigger used when we are deleting a client.
 * It will launch the procedure deleting the orders of the client.
 */
CREATE TRIGGER RecursiveDeleteClient BEFORE DELETE ON Clients EXECUTE PROCEDURE DeleteClient();

/*
 * The procedure used when we are deleting an order.
 * Deletes everything related to the order.
 */
CREATE OR REPLACE FUNCTION DeleteOrder() RETURNS TRIGGER AS $$
    BEGIN
      DELETE FROM OrderedDrinks WHERE orderNumber = OLD.orderNumber;
      RETURN NULL;
    END;
    $$LANGUAGE plpgsql;

/*
 * The trigger used when we are deleting an order.
 * It will launch the procedure deleting the orderedDrinks in that order.
 */
CREATE TRIGGER RecursiveDeleteOrder BEFORE DELETE ON Orders EXECUTE PROCEDURE DeleteOrder();




/*
 * PayTable 
 * DESC:  invoked by the smartphone on confirmation from the payment gateway (we ignore security on purpose here; a real app would never expose such an API, of course).
 * IN: a client token.
 * IN:  an amount paid.
 * OUT:
 * PRE: the client token is valid and corresponds to an occupied table.
 * PRE: the input amount is greater or equal to the amount due for that table.
 * POST: the table is released.
 * POST: the client token can no longer be used for ordering
 */
CREATE OR REPLACE FUNCTION PayTable(token integer, amount integer) RETURNS VOID AS $$
    DECLARE
      theTable integer;
      theAmountDue integer;
    BEGIN
      -- We start by verifying the preconditions.
      theTable = checkTable(token);
      SELECT INTO theAmountDue amountDue FROM Clients WHERE Clients.tokenNumber = token;
      IF amount < theAmountDue THEN
	RAISE EXCEPTION 'The amount payed (%) is not enough to pay what is due (%).', amount, theAmountDue;
      ELSE
        -- If the amount is enough, then the payement is added in the database.
        INSERT INTO Payements (amountPayed) VALUES (amount);
      END IF;

      -- The client token will non longer be used for ordering.
      DELETE FROM Clients WHERE tokenNumber = token;

      -- We update the table, because it is now free.
      UPDATE theTables SET isFree = true WHERE tokenNumber = token;
    
    END;
    $$LANGUAGE plpgsql;

SELECT PayTable(1,20);