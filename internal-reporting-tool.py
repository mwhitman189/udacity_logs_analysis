# Internal reporting tool for use with news website PostgeSQL databaseself. #This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Who the most popular articles are written by
#    3) On which days more than 1% of requests led to errors.


import bleach
import psycopg2

DBNAME = "news"

# Searches the database for the three most accessed articles


def top_articles():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    # Correlates article titles to slugs, then sums the number of views and groups by title and returns top 3.
    c.execute("select title, views from (select title, count(title) as views from articles left join log on slug = trim(leading '/article/' from path) group by title order by views desc) as sq limit 3;")
    return c.fetchall()
    c.close()
