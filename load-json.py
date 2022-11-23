from math import ceil
from os import system
import time
import pymongo
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
    start_time = time.time()
    client = pymongo.MongoClient('mongodb://localhost:' + port)
    db = client["291db"]
    collist = db.list_collection_names()
    if "dblp" in collist:
        db["dblp"].drop()
    system("mongoimport --port=" + port + " --db=291db --collection=dblp --file=" + filename)
    return db["dblp"]

def indexing():
    """
    create index
    """
    dblp = db["dblp"]
    dblp.create_index([("title", "text"),("authors","text"),("abstract","text"),("venue","text"),("year","text")])


def main():
    start_time = time.time()
    connect()
    indexing()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
