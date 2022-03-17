'''
    Desc: Object that has a connection to AGVN database and can return cursors.
    Using singleton pattern since its redundant and ineffecient to have multiple
    connections to the same database.
'''
from psycopg2 import connect

from .Singleton import Singleton


@Singleton
class DBConnection(object):

    def __init__(self):
        '''
        Class constructor creates a database connection to AGVN database.
        Raises ConnectionError if fails to connect to AGVN
        '''

        self.connect_db()

        if self.conn is None:
            raise ConnectionError('Failed to connect to AGVN database stores')

    def connect_db(self):
        '''
            Connect to PostgreSQL database and return version
        '''
        try:
            self.conn = connect(user="postgres",
                                password="password",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")
            self.cur = self.conn.cursor()

            self.cur.execute('SELECT version()')
            db_version = self.cur.fetchone()

        except Exception as e:
            print("Error connecting to DB:", e)

        return db_version

    def __del__(self):
        '''
        Class Deconstructor, closes connection to database when DBConnection is
        destroyed.
        '''

        self.conn.close()

    def cursor(self):
        '''
        Returns cursor to the AGVN data.
        '''

        return self.conn.cursor()
