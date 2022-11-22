"""Working in progress NOT DONE"""
def search_articles(dblp):
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
    for article in dblp.articleMatches.find():
        print(article)


def search_authors():
    pass


def list_venues():
    pass


def add_article():
    pass


if __name__ == "__main__":
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
