# Internal reporting tool for use with news website PostgeSQL databaseself. #This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Whom the most popular articles are written by
#    3) On which days more than 1% of requests led to errors.


import bleach
import psycopg2

DBNAME = "news"

# Searches the database for the three most accessed articles
# TODO: Create view for top article number of views


db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()
# c.execute("CREATE VIEW top_articles AS SELECT title, COUNT(title) AS views FROM articles LEFT JOIN log ON slug = trim(leading '/article/' from path) GROUP BY title ORDER BY views DESC;")
c.execute("CREATE VIEW auth AS SELECT name, id FROM authors;")
c.execute("CREATE VIEW art AS SELECT author, title, slug FROM articles;")
c.execute("CREATE VIEW logview AS SELECT path, status, time FROM log;")


def top_three_articles():
    c.execute("SELECT title, COUNT(title) AS views FROM art LEFT JOIN log ON slug = trim(leading '/article/' from path) GROUP BY title ORDER BY views DESC LIMIT 3;")
    top_three = c.fetchall()
    x = 1
    for article in top_three:
        print(str(x) + ") " + str(article))
        x += 1
    print("\n")
    c.close()


top_three_articles()


def top_authors():
    c = db.cursor()
    c.execute("SELECT name, COUNT(author) AS arts FROM art LEFT JOIN log ON slug = trim(leading '/article/' from path) JOIN auth ON auth.id = art.author GROUP BY name ORDER BY arts DESC;")
    top_auth = c.fetchall()
    x = 1
    for auth in top_auth:
        print(str(x) + ") " + str(auth))
        x += 1
    print("\n")
    c.close()


top_authors()


def req_err_days():
    c = db.cursor()
    c.execute("SELECT date_trunc('day', time) FROM logview;")
    date = c.fetchall()
    c.execute(
        "SELECT COUNT(status) FROM logview WHERE status NOT LIKE '2%' GROUP BY date_trunc('day', time);")
    daily_errors = c.fetchall()

    c.execute(
        "SELECT COUNT(status) FROM logview GROUP BY date_trunc('day', time);")
    daily_requests = c.fetchall()

    errors_n_requests = zip(date, daily_errors, daily_requests)

    for day, err, req in errors_n_requests:
        perc_daily_error = ((err[0] / req[0]) * 100)
        if perc_daily_error > 1.0:
            print(str(day[0]) + str(perc_daily_error))

    c.close()


req_err_days()
