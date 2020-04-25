PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Recipe;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS OrderedProductQnt;
DROP TABLE IF EXISTS Order;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Pallet;

PRAGMA foreign_keys = ON;

CREATE TABLE Ingredient(
    Ingredient_name    TEXT,
    QuantityStorage    INT,
    Unit    TEXT,
    LastDeliveryTime    DATETIME,
    LastDeliveryQuantity    INT,
    PRIMARY KEY(Ingredient_name)
);


CREATE TABLE Product(
    Product_name    TEXT,
    PRIMARY KEY(Product_name)
);

CREATE TABLE Recipe(
    Product_name    TEXT,
    Ingredient_name    TEXT,
    Quantity    INT,
    Unit    TEXT,
    PRIMARY KEY(Product_name, Ingredient_name),
    FOREIGN KEY(Product_name) REFERENCES Product(Product_name),
    FOREIGN KEY(Ingredient_name) REFERENCES Ingredient(Ingredient_name),
    FOREIGN KEY(Unit) REFERENCES Ingredient(Unit)   
);


CREATE TABLE Customer(
    Customerid    TEXT DEFAULT (lower(hex(randomblob(16)))),
    Name    TEXT,
    Address    TEXT,
    PRIMARY KEY(Customerid)
);

CREATE TABLE Order(
    Orderid    TEXT DEFAULT (lower(hex(randomblob(16)))),
    Customerid    TEXT,
    DeliveryDate   DATETIME,
    OrderDate    DATETIME,
    PRIMARY KEY(Orderid),
    FOREIGN KEY(Customerid) REFERENCES Customer(Customerid)
);

CREATE TABLE OrderedProductQnt(
    Product_name    TEXT,
    Orderid    TEXT,
    ProductQuantity    INT,
    PRIMARY KEY(Product_name, Order_id),
    FOREIGN KEY(Product_name) REFERENCES Product(Product_name),
    FOREIGN KEY(Orderid) REFERENCES Order(Orderid)
);

CREATE TABLE Pallet(
    Palletid    TEXT DEFAULT (lower(hex(randomblob(16)))),
    Product_name    TEXT,
    Orderid    TEXT,
    ProductionDate    DATETIME,
    DateDelivered    DATETIME,
    BlockedStatus    BOOLEAN,
    CurrentLocation    TEXT,
    PRIMARY KEY(Palletid),
    FOREIGN KEY(Product_name) REFERENCES Product(Product_name),
    FOREIGN KEY(Orderid) REFERENCES Order(Orderid)
);
