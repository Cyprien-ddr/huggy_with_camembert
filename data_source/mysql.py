import mysql.connector
from mysql.connector import Error
import sys
from bs4 import BeautifulSoup
from config import configs

def get_data():
    hats = []
    id_article = []
    try:
        connection = mysql.connector.connect(host=configs["database"]["mysql"]["host"],
                                             database=configs["database"]["mysql"]["db"],
                                             user=configs["database"]["mysql"]["user"],
                                             password=configs["database"]["mysql"]["password"])
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to Mysql Server version", db_info, end='\n')
            cursor = connection.cursor()
            cursor.execute("SELECT CONCAT(title, '\n',hat,'\n', content) AS data, id FROM post WHERE published = 1")
            rows = cursor.fetchall()

            id_article = [row[1] for row in rows]
            hats = [row[0] for row in rows]
            # Text clean -> we lost every html metadata
            # hats = [BeautifulSoup(row[0]).get_text() for row in rows]
            # hats = [row.replace("\n", "<br>") for row in hats]

    except Error as x:
        print("Error while connectiong to MySQL", x)
        sys.exit(1)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection close")
            return hats, id_article
