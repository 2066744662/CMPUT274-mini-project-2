"""MAY NEED MORE TESTS"""
import re

from pymongo import MongoClient

global dblp


def search_articles():
    keywords = []
    """Keywords input (case insensitive)"""
    while True:
        temp = input("Please enter the keyword you would like to search or :q to end the search: ")
        if temp == ":q":
            break
        else:
            keywords.append(re.compile(temp, re.IGNORECASE))

    """Clean the collection of search results"""
    dblp.articleMatches.drop()
    """search in database and add to collection of search results"""
    for keyword in keywords:
        for x in dblp.find({"$or": [{'authors': {"$regex": keyword}}, {'title': {"$regex": keyword}},
                               {'abstract': {"$regex": keyword}}, {'venue': {"$regex": keyword}},
                               {'year': {"$regex": keyword}}]}):
            if len(list(dblp.articleMatches.find({'id': x['id']}))) == 0:
                dblp.articleMatches.insert_one(x)
    """deal with duplicates"""
    dblp.articleMatches.aggregate([
        {"$group": {"_id": "$title", "count": {"$sum": 1}}},
        {"$match": {"_id": {"$ne": None}, "count": {"$gt": 1}}},
        {"$project": {"title": "$_id", "_id": 0}}
    ])
    """show results with order number to users for selection"""
    order = 1
    for article in dblp.articleMatches.find({}, {'_id': 0, 'id': 1, 'title': 1, 'year': 1, 'venue': 1}):
        print(str(order)+".", end="")
        print(article)
        order += 1
    id = input("Please enter the article id you would like to select: ")
    print("---------------------------------------")
    print("Selected Article: ")
    """info of selected article included abstract & venue"""
    for info in dblp.articleMatches.find({'id': id}, {'_id': 0, 'id': 1, 'title': 1, 'year': 1, 'venue': 1, 'abstract': 1, 'authors': 1}):
        print(info)
    """info of all references of selected article"""
    references = []
    for reference in dblp.articleMatches.find({'id': id}, {'references': 1, '_id': 0}):
        references.append(reference)
    print("---------------------------------------")
    print("References:")
    for reference in references[0]['references']:
        for r in dblp.find({'id': reference}, {'id': 1, 'title': 1, 'year': 1, '_id': 0}):
            print(r)


def search_authors():
    keyword = input("Please enter the keyword you would like to search: ")
    re_key = re.compile(keyword, re.IGNORECASE)
    """clear the authorsMatches collection"""
    dblp.authorsMatches.drop()
    """search all authors contained the keyword"""
    for author in dblp.find({'authors': {"$regex": re_key}}, {'authors': 1, 'title': 1, 'venue': 1, 'year': 1}):
        for target in author['authors']:
            if bool(re.search(keyword, target, re.IGNORECASE)):
                dblp.authorsMatches.insert_one(author)
                dblp.authorsMatches.update_one({'authors': {"$regex": re_key}}, {"$set": {'authors': target}})
    """sorted in descending order by year"""
    dblp.authorsMatches.find().sort('year', -1)
    authors = dblp.authorsMatches.find({}, {'_id': 0, 'authors': 1})
    """print out results"""
    print("Authors matched: \n")
    for author in authors:
        publications = dblp.authorsMatches.count_documents({'authors': author['authors']})
        print(author)
        print("Number of publications: ", end="")
        print(publications)
        print("---------------------------------------")
    """print out all publications of selected author"""
    selection = input("Please enter the name of author you would like to select: ")
    results = dblp.authorsMatches.find({'authors': selection}, {'_id': 0, 'title': 1, 'year': 1, 'venue': 1})
    for result in results:
        print(result)


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
