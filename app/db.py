import pymysql.cursors
import config

class DB():

    def __init__(self):
        self.db_params = config.db_params
        self.db_params['cursorclass'] = pymysql.cursors.DictCursor
        self.pefix = config.db_prefix

    def _create_connection(self):
        connection = pymysql.connect(**self.db_params)
        return connection

    def table(self, table_name):
        return self.pefix + table_name

    def exec(self, query, *args):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()
        connection.close()

    def getOne(self, query, *args):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone()
        connection.close()
        return result

    def getAll(self, query, *args):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        connection.close()
        return result