from math import ceil
from os import system
import time
import threading
import bson
import pymongo
global db, start_time

def connect():
    """
    Connect to MongoDB on given port and create 291db database.
    :param port: port number (string)
    :param filename: file name (string)
    :return: (Collection) pointing to the dblp collection
    """
    global db, start_time
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

def optimize():
    """
    generate token for each document
    """
    collist = db.list_collection_names()
    dblp = db["dblp"]
    total = dblp.count_documents({})
    threadLock = threading.Lock()
    threads = []
    thread1 = myThread(1, "Thread-1",total)
    thread2 = myThread(2, "Thread-2",total)
    thread1.start()
    thread2.start()
    threads.append(thread1)
    threads.append(thread2)
    for t in threads:
        t.join()

def tokenize(object):
    """
    Convert input into tokens.
    :param object: object to tonkenize
    :return: (set) set of tokens
    """
    if isinstance(object, list):
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

class myThread (threading.Thread):
    def __init__(self, threadID, name,total):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.total = total
    def run(self):
        if self.threadID == 1:
            results = db["dblp"].find().limit(int(self.total/2))
        else:
            results = db["dblp"].find().sort("_id",-1).limit(self.total - int(self.total/2))

        for result in results:
            values = list(result.values())
            token = str(tokenize(values))
            db["dblp"].update_one({"_id": values[0]}, {"$set": {"token": token}})
        print("--- %s seconds ---" % (time.time() - start_time))


def main():
    connect()
    optimize()


if __name__ == "__main__":
    main()
