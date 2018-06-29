# Internal reporting tool for use with news website PostgeSQL databaseself. #This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Who the most popular article authors are
#    3) On which days more than 1% of requests led to errors.


import bleach
import psycopg2

DBNAME = "news"

# Searches the database for the three most accessed articles
# TODO: Create view for top article number of views


db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()

c.execute(
    "CREATE INDEX idx_slug_path_comp ON log ((substr(path, length('/article/') + 1)));")


def top_three_articles():
    c.execute("SELECT title, COUNT(title) AS views FROM articles AS a RIGHT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1) GROUP BY title ORDER BY views DESC LIMIT 3;")
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
    c.execute("SELECT name, count(title) AS views FROM articles AS a LEFT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1) LEFT JOIN authors AS c ON a.author = c.id GROUP BY name ORDER BY views DESC;")
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

    c.execute(
        "SELECT to_char(date_trunc('day', time), 'Month dd, YYYY'), COUNT(id) FROM log WHERE status LIKE '4%' GROUP BY date_trunc('day', time);")
    daily_errors = c.fetchall()

    c.execute(
        "SELECT to_char(date_trunc('day', time), 'Month dd, YYYY'), COUNT(id) FROM log GROUP BY date_trunc('day', time);")
    daily_requests = c.fetchall()

    # Returns an iterator of tuples where each first/second/third... item is paired together
    errors_n_requests = zip(daily_errors, daily_requests)
    x = 0
    for err, req in errors_n_requests:
        perc_daily_error = ((err[1] / req[1]) * 100)
        date = err[0]
        if perc_daily_error > 1.0:
            if x == 0:
                print("The following dates had error rates over 1%:")
            print(str(date) + "  %Error:  " +
                  str("{: 0.2f}".format(perc_daily_error)))
            x += 1
    c.close()


req_err_days()
