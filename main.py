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

    """search in database and add to collection of search results"""
    results = dblp.find({"$text": {"$search": keywords}})
    
    """show results with order number to users for selection"""
    order = 0
    for article in articles:
        print("Article Matches: ")
        print("%d. ", order)
        print("ID: %s Title: %s Year: %s Venue: %s", article['_id']['id'], article['_id']['title'], article['_id']['year'], article['_id']['venue'])
        order += 1
    
    """user selection"""
    selection = articles[int(input("Please enter order number of the article you would like to select: "))]['_id']
    
    """info of selected article included abstract & venue"""
    print("---------------------------------------")
    print("Selected Article: ")
    print("ID: %s Title: %s Year: %s Venue: %s Abstract: %s Authors: %s", selection['id'], selection['title'], selection['year'], selection['venue'], selection['abstract'], selection['authors'])
    
    """info of all references of selected article"""
    references = []
    for ref_id in selection['references']:
        reference = dblp.find({'id': ref_id}, {'_id': 0, 'id': 1, 'title': 1, 'year': 1})
        references.append(reference)
    print("---------------------------------------")
    print("References:")
    for reference in references:
        print("ID: %s Title: %s Year: %s", reference['id'], reference['title'], reference['year'])


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
