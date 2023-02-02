import sqlite3
from sqlite3 import Error


class ConnAPI:
    def __init__(self, database):
        self.database = database
        self.conn = self.create_connection()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Error as e:
            print("Error! cannot create the database connection.")
            print(f"Error: {e}")

        return conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cur = self.conn.cursor()
            cur.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_data(self, sql_query, data):
        """
        Create a new project into the projects table
        :param data:
        :param sql_query:
        :param conn:
        :param project:
        :return: project id
        """
        cur = self.conn.cursor()
        try:
            cur.executemany(sql_query, data)
            self.conn.commit()
        except Error as e:
            print("Insert Error: ", e)
        return cur.lastrowid

    def get_data(self, sql_query):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute(sql_query)

        return cur.fetchall()