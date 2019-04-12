try:
    from config_custom import *
except:
    from config_default import *
from db import DB

# LANGUAGES
LANGUAGES = []
LANGUAGES_DATA = []
DEFAULT_LANGUAGE = False
db = DB()
query = """
    SELECT
        `code`,
        `name`,
        `is_default`,
        `order`,
        `added`,
        `is_active`
    FROM `{table}`
    ORDER BY `order` DESC
""".format(table=db.table('languages'))
connection = db.getConnection()
cursor = connection.cursor()
cursor.execute(query)
connection.close()
languages_data = cursor.fetchall()
if languages_data:
    for row in languages_data:
        LANGUAGES.append(row['code'])
        LANGUAGES_DATA.append(row)
        if row['is_default'] == 'Y' or not DEFAULT_LANGUAGE:
            DEFAULT_LANGUAGE = row['code']

# CURRENCIES
CURRENCIES = []
CURRENCIES_DATA = []
db = DB()
query = """
    SELECT
        `code`,
        `name`,
        `symbol`,
        `order`,
        `added`,
        `is_active`
    FROM `{table}`
    ORDER BY `order` DESC
""".format(table=db.table('currencies'))
connection = db.getConnection()
cursor = connection.cursor()
cursor.execute(query)
connection.close()
currencies_data = cursor.fetchall()
if currencies_data:
    for row in currencies_data:
        CURRENCIES.append(row['code'])
        CURRENCIES_DATA.append(row)
