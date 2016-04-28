
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
  tokenNumber integer primary key,
  amountDue integer
);

CREATE TABLE theTables (
  tableNumber integer primary key,
  codebar integer,
  isFree boolean
);

CREATE TABLE Orders (
  orderNumber integer primary key,
  orderTime timestamp
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
  quantity integer,
  primary key (orderNumber, drinkNumber),
  foreign key (orderNumber) references Orders (orderNumber),
  foreign key (drinkNumber) references Drinks (drinkNumber)
);

CREATE TABLE Payements (
  payementNumber integer primary key,
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

INSERT INTO Clients (tokenNumber, amountDue) VALUES
  (1, 20),
  (2, 30);

INSERT INTO theTables (tableNumber, codebar, isFree) VALUES
  (1, 10, false),
  (2, 20, false);

INSERT INTO Orders (orderNumber, orderTime) VALUES
  (1, '2016-04-28 12:59:01'),
  (2, '2016-04-28 13:10:22');

INSERT INTO Drinks (drinkNumber, price, name, description) VALUES
  (1, 1, 'water', 'simple water'),
  (2, 2, 'fanta', 'awesome fanta');

INSERT INTO OrderedDrinks (orderNumber, drinkNumber, quantity) VALUES
  (1, 2, 3),
  (2, 1, 4);

INSERT INTO Payements (payementNumber, amountPayed) VALUES
  (1, 10),
  (2, 400);

