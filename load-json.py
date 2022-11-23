from os import system
import time

import bson
from pymongo import MongoClient
global db

def connect():
    """
    Connect to MongoDB on given port and create 291db database.
    :param port: port number (string)
    :param filename: file name (string)
    :return: (Collection) pointing to the dblp collection
    """
    global db
    port = input("Input port number: ")
    filename = input("Input filename: ")
    client = MongoClient('mongodb://localhost:' + port)
    db = client["291db"]
    collist = db.list_collection_names()
    if "dblp" in collist:
        db["dblp"].drop()
    if "temp" in collist:
        db["temp"].drop()
    system("mongoimport --port=" + port + " --db=291db --collection=temp --file=" + filename)
    return db["temp"]

def optimize():
    start_time = time.time()
    collist = db.list_collection_names()
    temp = db["temp"]
    dblp = db["dblp"]
    results = temp.find()
    for result in results:
        values = list(result.values())
        token = str(tokenize(values))
        temp.update_one({"_id":values[0]},{"$set":{"token":token}})
    print("--- %s seconds ---" % (time.time() - start_time))


def tokenize(object):
    """
    Convert input into tokens.
    :param object: object to tonkenize
    :return: (set) set of tokens
    """
    if isinstance(object,list):
        s = set()
        for o in object:
            ret = tokenize(o)
            s = s.union(ret)
        return s
    elif isinstance(object, str):
        return set(object.split())
    elif isinstance(object, int):
        s = set()
        s.add(str(object))
        return s
    elif isinstance(object, bson.objectid.ObjectId):
        return set()
    else:
        raise Exception(str(type(object))+" is not expected :(")






def develope():
    global db
    print('delete me')
    client = MongoClient('mongodb://localhost:18372')
    db = client["291db"]

def main():
    connect()
    #develope()
    optimize()


if __name__ == "__main__":
    main()
