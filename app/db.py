import pymysql.cursors
import config

class DB():

    def __init__(self):
        self.db_params = config.db_params
        self.db_params['cursorclass'] = pymysql.cursors.DictCursor
        self.pefix = config.db_prefix

    def getConnection(self):
        return pymysql.connect(**self.db_params)

    def table(self, table_name):
        return self.pefix + table_name