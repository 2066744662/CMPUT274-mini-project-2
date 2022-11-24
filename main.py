"""MAY NEED MORE TESTS"""
import re

from pymongo import MongoClient
import pymongo

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
        if True:  # article not in articles.values():
            articles.update({order: article})
            order += 1

    """show results with order number to users for selection"""
    if not articles.keys():
        print("No results found!")
        return
    print("Article Matches: ")
    field2print = ["id", "title", "year", "venue"]
    for obj_id, article in zip(list(articles.keys()), list(articles.values())):
        print(obj_id, end=". ")
        print_article(article, field2print)
    """user selection"""
    user = input("Please enter order # of the article you would like to select: ")
    selection = articles[int(user)]

    """info of selected article included abstract & venue"""
    print("---------------------------------------")
    print("Selected Article: ")
    print_article(selection, div="\n")

    """info of all references of selected article"""
    print("---------------------------------------")
    print("This article is referenced by:")
    results = dblp.find({"references": selection["id"]})
    for r in results:
        print_article(r,["id","title","year"])
    print("---------------------------------------")


def search_authors():
        keyword = input("Please enter the keyword you would like to search: ")
    """search all authors contained the keyword"""
    authors = {}
    #results = dblp.find({'authors': {"$regex": re_key}},{'_id': 1, 'authors': 1, 'title': 1, 'venue': 1, 'year': 1}).sort('year', -1)
    results = dblp.find({"$text":{"$search": keyword}},{"score": { "$meta": "textScore"}}).sort('year', -1)
    for article in results:
        if article["score"] < 10:
            continue
        for author in article['authors']:
            if bool(re.search(keyword, author, re.IGNORECASE)):
                if author in authors.keys():
                    authors[author].append(article)
                else:
                    authors[author] = [article]
    """print out results"""
    print("Authors matched: \n")
    c = 0
    authors_keys = list(authors.keys())
    for author in authors_keys:
        c += 1
        print(c,": Name: ", author, " # of publications: ", len(authors[author]))
        print("---------------------------------------")
    """print out all publications of selected author"""
    while True:
        selection = input("Please enter the index of author you would like to select: ")
        try:
            articles = authors[authors_keys[int(selection)-1]]
            break
        except ValueError:
            print("Please input a number")
        except IndexError as e:
            print(e)
    for article in articles:
        print_article(article,["title","year","venue"],div="\n")
        print("")

def list_venues():
    venues = {}
    order = 1
    """user input to show top N venues"""
    amount = int(input("Please enter a number 'N' to see top N venues: "))
    for venue in dblp.aggregate(
            [{"$group": {"_id": "$venue", "Number_of_articles": {"$sum": 1}, "id": {"$first": "$id"}}},{"$limit": amount + 1}]):
        """{venue名称：[venue文章数, 引用venue文章的文章数]}"""
        venues.update({venue['_id']: [venue['Number_of_articles'], 0]})
    del venues['']
    dblp.articles.drop()
    """query of number of articles that reference a paper in that venue"""
    for venue in venues.keys():
        for temp in dblp.find({'venue': venue}, {'venue': 1, 'id': 1}):
            dblp.articles.insert_one(temp)
    for article in dblp.articles.find():
        for x in dblp.find({'references': {'$regex': article['id']}}):
            venues[article['venue']][1] += 1
    """sort by number of citations"""
    sorted_venues = sorted(venues.items(), key=lambda venues: venues[1][1], reverse=True)
    """print out results"""
    for venue in sorted_venues:
        print(order, ". Venue:", venue[0], "\n    Number of articles: ", venue[1][0], "\n    Number of articles that reference a paper in this venue: ", venue[1][1])
        order += 1


def add_article():
    """
    Add a record into collection. Info gather by user input
    """
    id = input("Id: ")
    title = input("Title: ")
    authors = []
    while True:
        author = input("Input one author at a time, or input ! if complete")
        if author == "!":
            if authors:
                break
            else:
                print("You have to input at least an author")
        else:
            authors.append(author)
    year = input("Year: ")
    while True:
        record = {"id": id,
                  "title": title,
                  "authors": authors,
                  "year": year,
                  "abstract": None,
                  "venue": None,
                  "references": [],
                  "n_citations": 0
                  }
        results = dblp.count_documents({"id":id})
        if results > 0:
            id = input("key is not unique. Input a unique key: ")
        else:
            dblp.insert_one(record)
            print("Saved")
            return


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


def print_article(article, fields=[], div=" | "):
    """
    print a dict in a pretty way
    :param article: (dict) object to print
    :param fields: optional:(list<string>) keys in the dict to print, empty list to print everything
    :param div: optional:(string) divider between each key and value pair
    """
    if not fields:
        fields = article.keys()
    for f in fields[:len(fields)-1]:
        if f == "_id":
            continue
        try:
            print(f, ' : ', article[f], end=div)
        except:
            continue
    print(fields[-1], ' : ', article[fields[-1]])


if __name__ == "__main__":
    port = input("Please input port number: ")
    connect(port)
    while True:
        print("_" * 30)
        print(
            "Welcome to the document store!\n1. Search for articles\n2. Search for authors\n3. List the venues\n4. Add "
            "an article\n5. End")
        print("_" * 30)
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
