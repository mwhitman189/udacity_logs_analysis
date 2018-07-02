# Internal reporting tool for use with news website PostgeSQL databaseself. #This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Who the most popular article authors are
#    3) On which days more than 1% of requests led to errors.


import os
import sys
import psycopg2

DBNAME = "news"

# Specify name given to report text file
FILENAME = "internal-log-report.txt"

# Create array of explanatory text for each query
ANSWER_TEXT = [
    '1. The three most popular articles of all time are:',
    '2. The most popular article authors are: ',
    '3. The following days had request errors rates over 1%:']

QUERIES = [
    ("""
    SELECT title, COUNT(title) AS views
    FROM articles AS a
    RIGHT JOIN log AS b
    ON a.slug = substr(b.path, length('/article/') + 1)
    GROUP BY title
    ORDER BY views DESC LIMIT 3;
    """),
    ("""
    SELECT name, COUNT(title) AS views
    FROM articles AS a
    LEFT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1)
    LEFT JOIN authors AS c ON a.author = c.id
    GROUP BY name
    ORDER BY views DESC;
    """),
    ("""
    SELECT sq.day, ROUND((100.0 * sq.daily_err / sq.total), 2) as error_perc
    FROM (SELECT to_char(date(log.time), 'Mon dd, yyyy') as day, count(id) as total, sum(case WHEN status !='200 OK' then 1 else 0 end) as daily_err
    FROM log
    GROUP BY day) as sq
    WHERE ROUND((100 * sq.daily_err / sq.total), 2) > 1;
    """)]



# Searches the database for the three most accessed articles
#c.execute("SELECT title, COUNT(title) AS views FROM articles AS a RIGHT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1) GROUP BY title ORDER BY views DESC LIMIT 3;")
#top_three = c.fetchall()
#x = 1
#for art in top_three:
#    print(str(x) + ") " + str(art))
#    x += 1
#print("\n")



#c.execute("SELECT name, COUNT(title) AS views FROM articles AS a LEFT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1) LEFT JOIN authors AS c ON a.author = c.id GROUP BY name ORDER BY views DESC;")
#top_auth = c.fetchall()
#x = 1
#for auth in top_auth:
#    print(str(x) + ") " + str(auth))
#    x += 1
#print("\n")



#c.execute("SELECT sq.day, ROUND((100.0 * sq.daily_err / sq.total), 2) as error_perc FROM (SELECT to_char(date(log.time), 'Mon dd, yyyy') as day, count(id) as total, sum(case WHEN status !='200 OK' then 1 else 0 end) as daily_err FROM log GROUP BY day) as sq WHERE ROUND((100 * sq.daily_err / sq.total), 2) > 1;")
#hi_error_days = c.fetchall()
#x = 1
#for day in hi_error_days:
#    print("The following days had errors on more than 1% of requests:")
#    print(str(x) + ") " + str(day[0]) + ": " + str(day[1]) + "%")
#    x += 1
#print("\n")
#c.close()

def conduct_analysis(queries):
    """
    Attempt to connect to 'news' database, create a results list, and iterate over queries printing the results.

    If unable to connect to the database, print the error and abort.
    """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        results = []

        for i in queries:
            c.execute(i)
            results.append(c.fetchall())
        db.close()

        return results
    except psycopg2.Error as error:
        print(error)
        sys.exit(1)


def answers(results):
    """
    """
    results = ''
    x = 0
    for i in results:
        if i[2]:
            results += ("x + ') '{res[0]}: {res[1]}%")
            x += 1
        else:
            for res in results:
                results += ("x + ') '{res[0]}: {res[1]}")
                x += 1


def output_to_file(analysis):
    """
    """
    f = open('./' + FILENAME, 'w')
    f.write(analysis)
    f.close()


if __name__ == "__main__":
    results = conduct_analysis(queries)
    analysis = answers(results)
    output_to_file(analysis)
    print('{} Successful'.format(FILENAME))
