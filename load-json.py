from os import system
from pymongo import MongoClient


def connect(port, filename):
    """
    Connect to MongoDB on given port and create 291db database.
    :param port: port number (string)
    :param filename: file name (string)
    :return: (Collection) pointing to the dblp collection
    """

    client = MongoClient('mongodb://localhost:' + port)
    db = client["291db"]
    collist = db.list_collection_names()
    print(collist)
    if "dblp" in collist:
        db["dblp"].drop()
    system("mongoimport --port=" + port + " --db=291db --collection=dblp --file=" + filename)
    return db["dblp"]


def main():
    port = input("Input port number: ")
    filename = input("Input filename: ")
    dblp = connect(port, filename)


if __name__ == "__main__":
    main()
