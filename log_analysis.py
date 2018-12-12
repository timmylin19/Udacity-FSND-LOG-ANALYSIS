import psycopg2


def find_top_three_articles(cur):
    cur.execute("SELECT SPLIT_PART(path, '/', 3) AS log_slug, count(*) \
        FROM log GROUP BY log_slug ORDER BY 2 DESC LIMIT 4")
    tp_3_articles = cur.fetchall()[1:]
    return [i[0] for i in tp_3_articles]


def find_top_three_authors(cur):
    cur.execute("CREATE VIEW Slug_count AS SELECT rank.log_slug, A.author, \
        rank.count FROM (SELECT split_part(path, '/', 3) AS log_slug, \
        count(*) FROM log GROUP BY log_slug ORDER BY 2 DESC) \
        AS rank, articles A WHERE rank.log_slug = A.slug")
    cur.execute("SELECT A.name, SUM(S.count) AS sum_cnt \
        FROM Slug_count S, authors A WHERE S.author = A.id \
        GROUP BY A.id ORDER BY sum_cnt DESC LIMIT 3")
    tp_3_authors = cur.fetchall()
    cur.execute("DROP VIEW Slug_count")
    return [i[0] for i in tp_3_authors]


def find_bad_request_days(cur):
    cur.execute("CREATE VIEW daily_requests AS SELECT  date(time), status, \
        count(status) FROM log GROUP BY date, status")
    cur.execute("SELECT TO_CHAR(T.date, 'YYYY-MM-DD') FROM \
        (SELECT A.date, A.count::float/B.count AS error_rate \
        FROM daily_requests AS A, daily_requests AS B WHERE A.date = B.date \
        AND A.status > B.status) AS T WHERE T.error_rate > 0.01")
    bay_request_days = cur.fetchall()
    cur.execute("DROP VIEW daily_requests")
    return [i[0] for i in bay_request_days]


def main():
    # Establish database connection
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()

    # Task 1 : Find three articles of all time
    tp_3_articles = find_top_three_articles(cur)
    print ("Three articles of all time:")
    print (tp_3_articles)

    # Task 2 : Who are the most popular article authors of all time
    tp_3_authors = find_top_three_authors(cur)
    print ("Most popular authors of all time")
    print (tp_3_authors)

    # Task 3 : Find days with > 1% request errors
    bad_request_days = find_bad_request_days(cur)
    print ("Days with more than 1 percent of request error rate")
    print (bad_request_days)

    # Close database connection
    db.close()


if __name__ == '__main__':
    main()
