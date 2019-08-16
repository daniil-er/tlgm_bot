import sqlite3


def connect_to(name_database):
    connection = sqlite3.connect(name_database)
    cursor = connection.cursor()

    return (connection, cursor)
