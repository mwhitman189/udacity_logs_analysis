#!/usr/bin/env python3

# Internal reporting tool for use with news website PostgreSQL database.
# This programs provides data on:
#    1) The 3 most popular articles of all time
#    2) Who the most popular article authors are
#    3) On which days more than 1% of requests led to errors.
# and outputs it in a txt file, 'internal-log-report.txt'.


import os
import sys
import psycopg2

DBNAME = "news"

# Specify name given to the report text file.
FILENAME = "internal-log-report.txt"

# Create an array of explanatory text for each query.
ANSWER_TEXT = [
    'The three most popular articles of all time are:',
    'The most popular article authors are:',
    'The following days had request errors rates over 1%:']

QUERIES = [
    # Select top the three articles based on the number of views (question 1).
    ("""
    SELECT title, COUNT(title) AS views
    FROM log AS b
    LEFT JOIN articles AS a
    ON a.slug = substr(b.path, length('/article/') + 1)
    GROUP BY title
    ORDER BY views DESC LIMIT 3;
    """),
    # Select the authors of the top three articles based on the number of views (question 2).
    ("""
    SELECT name, COUNT(title) AS views
    FROM articles AS a
    LEFT JOIN log AS b ON a.slug = substr(b.path, length('/article/') + 1)
    LEFT JOIN authors AS c ON a.author = c.id
    GROUP BY name
    ORDER BY views DESC LIMIT 3;
    """),
    # Select the days where the error percentage exceeded 1%.
    ("""
    SELECT sq.day, ROUND((100.0 * sq.daily_err / sq.total), 2) as error_perc
    FROM (SELECT to_char(date(log.time), 'Mon dd, yyyy') as day, count(id) as total, sum(case WHEN status !='200 OK' then 1 else 0 end) as daily_err
    FROM log
    GROUP BY day) as sq
    WHERE ROUND((100 * sq.daily_err / sq.total), 2) > 1;
    """)]


def conduct_analysis(queries):
    """
    Attempt to connect to the 'news' database, create a results list, and iterate over the queries, printing the results.

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


def output_to_file(analysis):
    """
    Open a text file.
    Write the output of 'conduct_analysis()' to the file.
    """
    f = open('./' + FILENAME, 'w')
    f.write(analysis)
    f.close()


def format_results_1(q_results):
    """
    Format the text of the results to be printed.
    Create an empty string, 'results'.
    Iterate through the results, adding 1 to variable 'x' to add rank numbers to results.
    """
    results = ''
    x = 1
    for res in q_results:
        results += ('   ' + str(x) +
                    ') "{}" — {} views\n').format(res[0], res[1])
        x += 1

    return results


def format_results_2(q_results):
    """
    Format the text of the results to be printed.
    Create an empty string, 'results'.
    Iterate through the results, adding 1 to variable 'x' to add rank numbers to results.
    """
    results = ''
    x = 1
    for res in q_results:
        results += ('   ' + str(x) +
                    ') {} — {} views\n').format(res[0], res[1])
        x += 1

    return results


def format_results_3(q_results):
    """
    Format the text of the results to be printed.
    Create an empty string, 'results'.
    Iterate through the results, adding 1 to variable 'x' to add rank numbers to 'results'.
    """
    results = ''
    x = 1
    for res in q_results:
        results += ('   ' + str(x) + ') {} — {}%\n').format(res[0], res[1])
        x += 1

    return results


def answers(ANSWER_TEXT):
    """
    Create an empty string, 'coll_results'.

    Iterate through list of answers, printing formatted text for the results.

        If on the top 3 articles, print the answer with double quotation marks around the article names.

        If on the daily error percentage, print the answer with a '%'.
    """
    coll_results = ''

    for i in range(len(ANSWER_TEXT)):
        coll_results += ANSWER_TEXT[i] + '\n'

        if i == 1:
            coll_results += format_results_2(q_results[i]) + '\n\n'
        elif i == 2:
            coll_results += format_results_3(q_results[i]) + '\n\n'
        else:
            coll_results += format_results_1(q_results[i]) + '\n\n'

    return coll_results


if __name__ == "__main__":
    """
    Assign the query function to 'q_results'.
    Assign the analysis function to 'analysis'.
    Call the output function.
    Print '<FILENAME> Successful'.
    """
    q_results = conduct_analysis(QUERIES)
    analysis = answers(ANSWER_TEXT)
    output_to_file(analysis)
    print('{} Successful'.format(FILENAME))
