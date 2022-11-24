from os import system

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

    client = pymongo.MongoClient('mongodb://localhost:' + port)
    db = client["291db"]
    collist = db.list_collection_names()
    if "dblp" in collist:
        db["dblp"].drop()
    system("mongoimport --port=" + port + " --db=291db --collection=dblp --file=" + filename)
    return db["dblp"]

def indexing():
    """
    create indexes
    """
    dblp = db["dblp"]
    dblp.create_index([("title", "text"),("authors","text"),("abstract","text"),("venue","text"),("year","text")],weights={"authors":90000,"title":1,"abstract":1,"venue":1,"year":1})
    dblp.create_index([("authors", 1)])
    dblp.create_index([("references", 1)])

def main():
    connect()
    indexing()



if __name__ == "__main__":
    main()
