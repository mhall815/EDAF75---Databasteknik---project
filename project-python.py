from bottle import get, post, run, request, response
import sqlite3
import json
from sqlite3 import OperationalError

HOST = 'localhost'
PORT = 8888

conn = sqlite3.connect("create-schema.db")


def url(resource):
    return "http://{}:{}{}".format(HOST, PORT, resource)


def format_response(d):
    return json.dumps(d, indent=4) + "\n"


def executeScriptsFromFile(filename):
    c = conn.cursor()
    # Opens and reads the file in question.
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            c.execute(command)
        except OperationalError, msg:
            print
            "Command skipped: ", msg


@get('/ping')
def get_ping():
    response.status = 200
    return "pong \n"


@get('/customer')
def get_customer():
    c = conn.cursor()
    c.execute(
        """
            SELECT Name, Address, CustomerId
            FROM Customer
        """
    )
    s = [{"name": Name, "Address": Address, "CustomerId": CustomerId}
         for (Name, Address, CustomerId) in c]

    response.status = 200
    return json.dumps({"customers": s}, indent=4)


@get('/ingredients')
def get_ingredients():
    c = conn.cursor()
    c.execute(
        """
            SELECT Ingredient_name, QuantityStorage, Unit
            FROM Ingredient
        """
    )
    s = [{"name": Ingredient_name, "quantity": QuantityStorage, "unit": Unit}
         for (Ingredient_name, QuantityStorage, Unit) in c]

    response.status = 200
    return json.dumps({"ingredients": s}, indent=4)

@get('/cookies')
def get_cookies():
    c = conn.cursor()
    c.execute(
        """
            SELECT Product_name
            FROM Product
        """
    )
    s = [{"name" :Product_name}
         for (Product_name) in c]

    response.status = 200
    return json.dumps({"cookies": s}, indent=4)

@get('/recipes')
#Simple get recipes.
def get_recipes():
    c = conn.cursor()
    c.execute(
        """
        SELECT Product_name, Ingredient_name, Quantity, Unit
        FROM Recipe
        INNER JOIN Ingredient
        USING(Ingredient_name)
        """
    )
    s = [{"cooke" :Product_name,"ingredient":Ingredient_name, "quantity": Quantity,"unit": Unit}
         for (Product_name, Ingredient_name, Quantity, Unit) in c]

    response.status = 200
    return json.dumps({"recipes": s}, indent=4)

@post('/pallets')
def post_pallets():
    response.content_type = 'application/json'

    cookie = request.query.cookie

    if not (cookie):
        response.status = 400
        return json.dump({"error": "missing parameter"}, indent=4)


    try:
        c = conn.cursor()
        c.execute(
            """
            SELECT Product_name
            FROM Product
            WHERE Product_name = ?
            """,
            [cookie]
        )
        check = c.fetchone()[0]
    except:
        return json.dumps({"status":"no such cookie"}, indent = 4)

    #loopa igenom produktens ingredienser och kor checkingredients.
    c.execute("""
    SELECT Ingredient_name, Quantity
    FROM Recipe
    WHERE Product_name = ?
    """, [cookie])
    ingreds =  c.fetchall()
    #the wished ingredients and the quantities of them are now in an arraylist. Now we wish to run them through the checkIngredients
    #function to check if there are enough ingredients to produce the pallet.
    x = [(1, 2), (3, 4), (5, 6)]

    for a, b in x:
        print(a, "plus", b, "equals", a + b)
    for IngName,Quant in ingreds:
        if (checkIngredients(IngName,Quant) < 0):
            response.status = 400
            return json.dumps({"status": "not enough ingredients"}, indent=4)


    return json.dumps({"status": "ok"}, indent=4)


def checkIngredients(Ingredient, Quantity):
    #We compare quantity that is to be withdrawn with the current quantity of the storage. Multiply quantity by 54 to get amount for
    #5400 cookies and not for 100 cookies.
    Quantity = Quantity*54
    c = conn.cursor()
    c.execute("""
    SELECT QuantityStorage
    FROM Ingredient
    WHERE Ingredient_name = ?
    -
    ?
    """,[Ingredient, Quantity]
              )
    return c.fetchone()[0]





# curl -X POST http://localhost:8888/pallets\?cookie\=Berliner
# create a new pallet with cookie berliner
# if no cookie return status
# if not enough ingred return status
# if all good return ok
# newly created pallets have blocked status false and can have customer as null.


@get('/pallets')
def get_pallets():
    c = conn.cursor()
    c.execute(
        """
        SELECT Palletid, Product_name, ProductionDate, Name, BlockedStatus
        FROM Pallet
        INNER JOIN Order
        USING(OrderId)
        INNER JOIN Customer
        USING(CustomerId)
        """
    )
    s = [{"id":Palletid, "cookie":Product_name, "productionDate":ProductionDate,"customer":Name, "blocked":BlockedStatus}
         for (Palletid,Product_name,ProductionDate, Name, BlockedStatus) in c]



    response.status = 200
    return json.dumps({"pallets": s}, indent=4)
#simple get pallets. See if blocked or not as well.
#curl -X GET http://localhost:8888/pallets\?cookie\=Amneris\&blocked\=0\&after\=2020-03-03
# extra parameters are "blocked" see only blocked pallets, "after" get pallets produced after date.
# "before" restricts search to before date. "cookie" gets pallet of specific cookie

@post('/block')
# curl -X POST http://localhost:8888/block/<cookie-name>/<from-date>/<to-date>
# blocks specific cookie produced during form-date to to-date.
#change blocked status to true if cookie name and is produced during specific date.



@post('/unblock')
#unblocks cookies from dates to dates. Similar as before but with unblock insted.





@post('/reset')
def reset():
    executeScriptsFromFile('initial-data.sql')

    conn.commit()
    response.status = 200
    return 'ok \n'


run(host=HOST, port=PORT, debug=True)