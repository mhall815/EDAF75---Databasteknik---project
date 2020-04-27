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
        except OperationalError as msg:
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
    s = [{"name": Product_name}
         for (Product_name) in c]

    response.status = 200
    return json.dumps({"cookies": s}, indent=4)


@get('/recipes')
# Simple get recipes.
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
    s = [{"cookie": Product_name, "ingredient": Ingredient_name, "quantity": Quantity, "unit": Unit}
         for (Product_name, Ingredient_name, Quantity, Unit) in c]

    response.status = 200
    return json.dumps({"recipes": s}, indent=4)


# curl -X POST http://localhost:8888/pallets\?cookie\=Berliner
# create a new pallet with cookie berliner
# if no cookie return status
# if not enough ingred return status
# if all good return ok
# newly created pallets have blocked status false and can have customer as null.
@post('/pallets')
def post_pallets():
    response.content_type = 'application/json'

    cookie = request.query.cookie

    if not cookie:
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
        return json.dumps({"status": "no such cookie"}, indent=4)

    # loopa igenom produktens ingredienser och kor checkingredients.
    c.execute(
        """
    SELECT Ingredient_name
    FROM Recipe
    INNER JOIN Ingredient
    USING(Ingredient_name)
    WHERE Product_name = ? AND (QuantityStorage - Quantity*54 <0 OR QuantityStorage is NULL)
    """, [cookie])
    # We get the differences and put them into a list.
    Ingreds = c.fetchall()
    if Ingreds:
        return json.dumps({"status": "not enough ingredients"})

    # Kor programmet, skapar en pallet och drar bort quantity fran storage.
    c.execute(
        """
        INSERT INTO Pallet(Palletid, Product_name, ProductionDate)
        VALUES(lower(hex(randomblob(16))), ?, CURRENT_DATE )
        RETURNING Palletid;
        
        SELECT Palletid
        FROM Pallet
        WHERE rowid = last_insert_rowid()
        """, [cookie]
    )
    get_Palletid = c.fetchone()[0]
    print(get_Palletid)



    return json.dumps({"status": "ok", "id": get_Palletid })


# simple get pallets. See if blocked or not as well.
# curl -X GET http://localhost:8888/pallets\?cookie\=Amneris\&blocked\=0\&after\=2020-03-03
# extra parameters are "blocked" see only blocked pallets, "after" get pallets produced after date.
# "before" restricts search to before date. "cookie" gets pallet of specific cookie
@get('/pallets')
def get_pallets():
    c = conn.cursor()
    c.execute(
        """
        SELECT Palletid, Product_name, ProductionDate, BlockedStatus
        FROM Pallet

        """
    )
    s = [{"id": Palletid, "cookie": Product_name, "productionDate": ProductionDate,
          "blocked": BlockedStatus}
         for (Palletid, Product_name, ProductionDate, BlockedStatus) in c]

    response.status = 200
    return json.dumps({"pallets": s}, indent=4)


# curl -X POST http://localhost:8888/block/<cookie-name>/<from-date>/<to-date>
# blocks specific cookie produced during form-date to to-date.
# change blocked status to true if cookie name and is produced during specific date.
@post('/block')
def post_block():
    response.content_type = 'application/json'

    cookie = request.query.cookie
    from_date = request.query.from_date
    to_date = request.query.to_date

    if not (cookie and from_date and to_date):
        response.status = 400
        return json.dump({"error": "missing parameter"}, indent=4)

    try:
        c = conn.cursor()
        c.execute(
            """
            UPDATE Pallet
            SET
                BlockedStatus = true
            WHERE Product_name = ? AND  ProductionDate > ? AND ProductionDate < ?
            """,
            [cookie, from_date, to_date]
        )
        check = c.fetchone()[0]
    except:
        return json.dumps({"status": "no such cookie"}, indent=4)


@post('/unblock')
# unblocks cookies from dates to dates. Similar as before but with unblock insted.

@post('/reset')
def reset():
    executeScriptsFromFile('initial-data.sql')

    conn.commit()
    response.status = 200
    return 'ok \n'


run(host=HOST, port=PORT, debug=True)