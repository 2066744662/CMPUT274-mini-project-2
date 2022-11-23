"""MAY NEED MORE TESTS"""
import re

from pymongo import MongoClient

global dblp


def search_articles():
    keywords = ""

    """Keywords input (case insensitive)"""
    while True:
        t = input("Please enter the keyword you would like to search or :q to end the search: ")
        if t == ":q":
            break
        else:
            keywords += "\"" + t + "\""
    if keywords == "":
        return

    articles = {}
    order = 1
    """search in database and add to collection of search results"""
    for article in dblp.find({"$text": {"$search": keywords}}):
        if article not in articles.values():
            articles.update({order: article})
            order += 1

    """show results with order number to users for selection"""
    print("Article Matches: ")
    for obj_id, article in zip(list(articles.keys()), list(articles.values())):
        del article['_id']
        print(obj_id, ". ", article)

    """user selection"""
    user = input("Please enter order # of the article you would like to select: ")
    selection = articles[int(user)]

    """info of selected article included abstract & venue"""
    print("---------------------------------------")
    print("Selected Article: ")
    print(selection)

    """info of all references of selected article"""
    references = {}
    order = 1
    for ref_id in selection['references']:
        for reference in dblp.find({'id': ref_id}, {'_id': 0, 'id': 1, 'title': 1, 'year': 1}):
            references.update({order: reference})
            order += 1
    print("---------------------------------------")
    print("References:")
    for order, reference in zip(list(references.keys()), list(references.values())):
        print(order, ". ", reference)


def list_venues():
    pass


def add_article():
    pass

def connect(port):
    """
    connect to the Mongodb dblp collection, save into global variable
    :param port: (String) port number of MongoDB connection
    """
    global dblp
    try:
        client = MongoClient('mongodb://localhost:' + port)
    except ValueError as e:
        print(e)
        port1 = input("Please input port number: ")
        connect(port1)
        return
    db = client["291db"]
    collist = db.list_collection_names()
    if "dblp" not in collist:
        raise Exception("dblp not found")
    dblp = db["dblp"]

if __name__ == "__main__":
    port = input("Please input port number: ")
    connect(port)
    print("_"*30)
    print("Welcome to the document store!\n1. Search for articles\n2. Search for authors\n3. List the venues\n4. Add "
          "an article\n5. End")
    print("_"*30)
    while True:
        i = input("Please choose a number (1-5): ")
        match i:
            case "1":
                search_articles()
            case "2":
                search_authors()
            case "3":
                list_venues()
            case "4":
                add_article()
            case "5":
                break
            case _:
                print("Error input.")
    print("End.")
