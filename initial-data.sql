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
INTO    Ingredient(Ingredient_name, QuantityStorage, unit)
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
INTO    Recipe(Product_name, Ingredient_name, Quantity, Unit)
VALUES    ("Nut Ring", "Flour", 450, "g"),
    ("Nut ring", "Butter", 450, "g"),
    ("Nut ring", "Icing sugar", 190, "g"),
    ("Nut ring", "Roasted, chopped nuts", 450, "g"),
    ("Nut cookie", "Fine-ground nuts", 750, "g"),
    ("Nut cookie", "Ground, roasted nuts", 625, "g"),
    ("Nut cookie", "Bread crumbs", 125, "g"),
    ("Nut cookie", "Sugar", 375, "g"),
    ("Nut cookie", "Egg whites", 3.5, "dl"),
    ("Nut cookie", "Chocolate", 50, "g"),
    ("Amneris", "Marzipan", 750, "g"),
    ("Amneris", "Butter", 250, "g"),
    ("Amneris", "Eggs", 250, "g"),
    ("Amneris", "Potato starch", 25, "g"),
    ("Amneris", "Wheat flour", 25, "g"),
    ("Tango", "Butter", 200, "g"),
    ("Tango", "Sugar", 250, "g"),
    ("Tango", "Flour", 300, "g"),
    ("Tango", "Sodium bicarbonate", 4, "g"),
    ("Tango", "Vanilla", 2, "g"),
    ("Almond delight", "Butter", 400, "g"),
    ("Almond delight", "Sugar", 270, "g"),
    ("Almond delight", "Chopped almonds", 279, "g"),
    ("Almond delight", "Flour", 400, "g"),
    ("Almond delight", "Cinnamon", 10, "g"),
    ("Berliner", "Flour", 350, "g"),
    ("Berliner", "Butter", 250, "g"),
    ("Berliner", "Icing sugar", 100, "g"),
    ("Berliner", "Eggs", 50, "g"),
    ("Berliner", "Vanilla sugar", 5, "g"),
    ("Berliner", "Chocolate", 50, "g");
