#!/usr/bin/python3
import re
import mysql.connector
from bs4 import BeautifulSoup
from mysql.connector import Error
import sys
from config import configs


def exclude_content_between_a_tags(text: str) -> str:
    """
    Excludes content between the tags specified in text and returns them as a string

    :param text: text to be filtered
    :return: string of text filtered
    """

    pattern = re.compile(r'<a[^>]*>.*?</a>', re.DOTALL)
    result = re.sub(pattern, '', text)

    return result


def update_db(current: list[dict]) -> None:
    """
    Update the database.txt with current data from MySQL into the database.txt
    :param current: new data to update
    :return:
    """
    fpath = configs['database.txt']['fpath']
    fd = open(fpath, "w")
    fd.write("")
    fd.close()
    fd = open(fpath, "a")
    for line in current:
        fd.write(f'{str(line)}\n')
    fd.close()


def get_data() -> list[dict]:
    """
    Connect to a MySQL database.txt, retrieves data from a specific table.

    :return: A list of dictionaries, where each dictionary represents a row from the "post" table in the MySQL database.txt. Each dictionary contains the id, hat, and content values.
    """
    db = []
    try:
        connection = mysql.connector.connect(host=configs["database"]["mysql"]["host"],
                                             database=configs["database"]["mysql"]["db"],
                                             user=configs["database"]["mysql"]["user"],
                                             password=configs["database"]["mysql"]["password"])
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to Mysql Server version", db_info, end='\n')
            cursor = connection.cursor()
            cursor.execute("SELECT hat, id, title, content FROM post WHERE published = 1")
            rows = cursor.fetchall()
            db = [
                {
                    'id': row[1],
                    'hat': BeautifulSoup(exclude_content_between_a_tags(row[0])).get_text().replace('\xa0', ' '),
                    'html_hat': row[0],
                    'title': row[2],

                }
                for row in rows
            ]

    except Error as x:
        print("Error while connectiong to MySQL", x)
        sys.exit(1)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection close")
    return db
