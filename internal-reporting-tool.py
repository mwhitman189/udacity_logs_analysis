# Internal reporting tool for use with news website PostgeSQL databaseself. #This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Whom the most popular articles are written by
#    3) On which days more than 1% of requests led to errors.


import bleach
import psycopg2

DBNAME = "news"

# Searches the database for the three most accessed articles
# TODO: Create view for top article number of views


def top_articles():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    # Correlates article titles to slugs, then sums the number of views and groups by title and returns top 3.
    c.execute("select title, views from (select title, count(title) as views from articles left join log on slug = trim(leading '/article/' from path) group by title order by views desc) as sq limit 3;")
    top_three = c.fetchall()
    x = 1
    for article in top_three:
        print(str(x) + ") " + str(article))
        x += 1
    print("\n")
    c.close()


top_articles()


def top_authors():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute("select author, title, count(title) as views from articles left join log on slug = trim(leading '/article/' from path) group by author, title order by views desc;")
    top_three_authors = c.fetchall()
    x = 1
    for author in top_three_authors:
        print(str(x) + ") " + str(author))
        x += 1
    print("\n")
    c.close()


top_authors()
