DROP TABLE IF EXISTS Client CASCADE;
DROP TABLE IF EXISTS theTable CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Drink CASCADE;
DROP TABLE IF EXISTS OrderedDrink CASCADE;
DROP TABLE IF EXISTS Payement CASCADE;

CREATE TABLE Client (
  tokenNumber integer primary key,
  amountDue integer
);

CREATE TABLE theTable (
  tableNumber integer primary key,
  codebar integer,
  isFree boolean
);

CREATE TABLE Orders (
  orderNumber integer primary key,
  orderTime timestamp
);

CREATE TABLE Drink (
  drinkNumber integer primary key,
  price integer,
  name varchar(20),
  description varchar(100)
);

CREATE TABLE OrderedDrink (
  orderNumber integer,
  drinkNumber integer,
  qty integer,
  primary key (orderNumber, drinkNumber),
  foreign key (orderNumber) references Orders (orderNumber),
  foreign key (drinkNumber) references Drink (drinkNumber)
);

CREATE TABLE Payement (
  payementNumber integer primary key,
  amountPayed integer
);