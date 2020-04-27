from bottle import get, post, run, request, response
import sqlite3
import json
from sqlite3 import OperationalError

HOST = 'localhost'
PORT = 8888

conn = sqlite3.connect("create-schema.db")


def url(resource):
    return f"http://{HOST}:{PORT}{resource}"


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
            SELECT Name, Address
            FROM Customer
        """
    )
    s = [{"name": Name, "Address": Address}
         for (Name, Address) in c]

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
         for (Product_name,) in c]
    return json.dumps({"cookies":s}, indent=4)


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
        VALUES(lower(hex(randomblob(16))), ?, CURRENT_DATE)
        """, [cookie]
    )
    c.execute(
        """
        SELECT Palletid
        FROM Pallet
        WHERE rowid = last_insert_rowid()
        """
    )
    get_Palletid = c.fetchone()[0]
    return json.dumps({"status": "ok", "id": get_Palletid})


# simple get pallets. See if blocked or not as

# curl -X GET http://localhost:8888/pallets\?cookie\=Amneris\&blocked\=0\&after\=2020-03-03
# extra parameters are "blocked" see only blocked pallets, "after" get pallets produced after date.
# "before" restricts search to before date. "cookie" gets pallet of specific cookie
@get('/pallets')
def get_pallets():
    c = conn.cursor()
    c.execute(
        """
        SELECT Palletid, Product_name, ProductionDate, Name, 
        CASE WHEN BlockedStatus= 0 THEN 'false' ELSE 'true' END as blocked 
        FROM Pallet
        LEFT JOIN Orders
        USING(Orderid)
        LEFT JOIN Customer
        USING(Customerid)

        """
    )
    s = [{"id": Palletid, "cookie": Product_name, "productionDate": ProductionDate, "customer": Name,
          "blocked": blocked}
         for (Palletid, Product_name, ProductionDate, Name, blocked) in c]

    response.status = 200
    return json.dumps({"pallets": s}, indent=4)


# curl -X POST http://localhost:8888/block/<cookie-name>/<from-date>/<to-date>
# blocks specific cookie produced during form-date to to-date.
# change blocked status to true if cookie name and is produced during specific date.
@post('/block/<cookie>/<from_date>/<to_date>')
def post_block(cookie, from_date, to_date):
    response.content_type = 'application/json'

    if not (cookie and from_date and to_date):
        response.status = 400
        return json.dump({"error": "missing parameter"}, indent=4)

    try:
        c = conn.cursor()
        c.execute(
            """
            UPDATE Pallet
            SET
                BlockedStatus = 1
            WHERE Product_name = ? AND  ProductionDate > ? AND ProductionDate < ?
            """,
            [cookie, from_date, to_date]
        )
    except:
        return json.dumps({"status": "no such cookie"}, indent=4)

    return json.dumps({"status": "such cookie"}, indent=4)


@post('/unblock/<cookie>/<from_date>/<to_date>')
def post_block(cookie, from_date, to_date):
    response.content_type = 'application/json'

    if not (cookie and from_date and to_date):
        response.status = 400
        return json.dump({"error": "missing parameter"}, indent=4)

    try:
        c = conn.cursor()
        c.execute(
            """
            UPDATE Pallet
            SET
                BlockedStatus = 0
            WHERE Product_name = ? AND  ProductionDate > ? AND ProductionDate < ?
            """,
            [cookie, from_date, to_date]
        )
    except:
        return json.dumps({"status": "no such cookie"}, indent=4)

    return json.dumps({"status": "such cookie"}, indent=4)


# unblocks cookies from dates to dates. Similar as before but with unblock insted.



@post('/reset')
def reset():
    executeScriptsFromFile('initial-data.sql')

    conn.commit()
    return json.dumps({"status": "ok"}, indent=4)


run(host=HOST, port=PORT, debug=True)
