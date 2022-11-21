def search_articles():
    pass


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