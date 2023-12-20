import pymysql
import sys
from bs4 import BeautifulSoup


def connection_to_db():
    hats = []
    id_article = []
    connection = None
    try:
        connection = pymysql.connect(host='localhost',
                                     database='website',
                                     user='root',
                                     password='db_on_docker')

        print("Connected to Mysql Server", end='\n')
        cursor = connection.cursor()
        cursor.execute('SELECT CONCAT(title, \'\n\',hat) AS data, id FROM post')
        rows = cursor.fetchall()
        id_article = [row[1] for row in rows]
        hats = [BeautifulSoup(row[0], "lxml").text for row in rows]
        hats = [row.replace("\n", "<br>") for row in hats]

    except Exception as x:
        print("Error while connectiong to MySQL", x)
        sys.exit(1)
    finally:
        connection.close()
        print("MySQL connection closed")
        return hats, id_article
