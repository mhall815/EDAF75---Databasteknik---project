from bottle import get, post, run, request, response
import sqlite3
import json
from sqlite3 import OperationalError
HOST = 'localhost'
PORT = 1234
#TEST


conn = sqlite3.connect("create-schema.db")


def url(resource):
    return "http://{}:{}{}".format(HOST, PORT,resource)

def format_response(d):
    return json.dumps(d, indent=4) + "\n"

def executeScriptsFromFile(filename):
    c = conn.cursor()
    #Opens and reads the file in question.
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close() 
    
    sqlCommands = sqlFile.split(';')
    
    for command in sqlCommands:
        try:
            c.execute(command)
        except OperationalError, msg:
            print "Command skipped: ", msg


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
    s = [{"Name": Name, "Address":Address}
        for(Name, Address) in c]

    response.status = 200
    return json.dumps({"data" : s}, indent= 4)







@post('/reset')
def reset():

    executeScriptsFromFile('initial-data.sql')

    conn.commit()
    response.status = 200
    return 'ok \n'
    


run(host=HOST, port=PORT, debug=True)