import pymysql.cursors
import config

class DB():

    def __init__(self):
        self.db_params = config.DB_PARAMS
        self.db_params['cursorclass'] = pymysql.cursors.DictCursor
        self.pefix = config.DB_PREFIX

    def getConnection(self):
        return pymysql.connect(**self.db_params)

    def table(self, table_name):
        return self.pefix + table_name