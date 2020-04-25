INSERT
INTO    Customer(Customerid, Name, Address)
VALUES    (lower(hex(randomblob(16))), "Finkakor AB", "Helsingborg"),
    (lower(hex(randomblob(16))), "Småbröd AB", "Malmö"),
    (lower(hex(randomblob(16))), "Kaffebröd AB", "Landskrona"),
    (lower(hex(randomblob(16))), "Bjudkakor AB", "Ystad"),
    (lower(hex(randomblob(16))), "Kalaskakor AB", "Trelleborg"),
    (lower(hex(randomblob(16))), "Partykakor AB", "Kristianstad"),
    (lower(hex(randomblob(16))), "Gästkakor AB", "Hässleholm"),
    (lower(hex(randomblob(16))), "Skånekakor AB", "Perstop");

INSERT 
INTO    Product(Product_name)
VALUES    ("Nut ring"),
    ("Nut cookie"),
    ("Amneris"),
    ("Tango"),
    ("Almond delight"),
    ("Berliner");

INSERT
INTO    Ingredient(Ingredient_name, QuantityStorage, Unit)
VALUES    ("Flour", 100000, "g"),
    ("Butter", 100000, "g"),
    ("Icing sugar", 100000, "g"),
    ("Roasted, chopped nuts", 100000, "g"),
    ("Fine-ground nuts", 100000, "g"),
    ("Ground, roasted nuts", 100000, "g"),
    ("Bread crumbs", 100000, "g"),
    ("Sugar", 100000, "g"),
    ("Egg whites", 100000, "ml"),
    ("Chocolate", 100000, "g"),
    ("Marzipan", 100000, "g"),
    ("Eggs", 100000, "g"),
    ("Potato starch", 100000, "g"),
    ("Wheat flour", 100000, "g"),
    ("Sodium bicarbonate", 100000, "g"),
    ("Vanilla", 100000, "g"),
    ("Chopped almonds", 100000, "g"),
    ("Cinnamon", 100000, "g"),
    ("Vanilla sugar", 100000, "g");



INSERT 
INTO    Recipe(Product_name, Ingredient_name, Quantity)
VALUES    ("Nut Ring", "Flour", 450),
    ("Nut ring", "Butter", 450),
    ("Nut ring", "Icing sugar", 190),
    ("Nut ring", "Roasted, chopped nuts", 450),
    ("Nut cookie", "Fine-ground nuts", 750),
    ("Nut cookie", "Ground, roasted nuts", 625),
    ("Nut cookie", "Bread crumbs", 125),
    ("Nut cookie", "Sugar", 375),
    ("Nut cookie", "Egg whites", 350),
    ("Nut cookie", "Chocolate", 50),
    ("Amneris", "Marzipan", 750),
    ("Amneris", "Butter", 250),
    ("Amneris", "Eggs", 250),
    ("Amneris", "Potato starch", 25),
    ("Amneris", "Wheat flour", 25),
    ("Tango", "Butter", 200),
    ("Tango", "Sugar", 250),
    ("Tango", "Flour", 300),
    ("Tango", "Sodium bicarbonate", 4),
    ("Tango", "Vanilla", 2),
    ("Almond delight", "Butter", 400),
    ("Almond delight", "Sugar", 270),
    ("Almond delight", "Chopped almonds", 279),
    ("Almond delight", "Flour", 400),
    ("Almond delight", "Cinnamon", 10),
    ("Berliner", "Flour", 350),
    ("Berliner", "Butter", 250),
    ("Berliner", "Icing sugar", 100),
    ("Berliner", "Eggs", 50),
    ("Berliner", "Vanilla sugar", 5),
    ("Berliner", "Chocolate", 50);
