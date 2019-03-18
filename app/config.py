try:
    from config_custom import *
except:
    from config_default import *
from db import DB

# LANGUAGES
db = DB()
query = 'SELECT `code`, `is_default` FROM `{table}`'.format(table=db.table('languages'))
connection = db.getConnection()
cursor = connection.cursor()
cursor.execute(query)
connection.close()
LANGUAGES = []
DEFAULT_LANGUAGE = False
languages_data = cursor.fetchall()
if languages_data:
    for row in languages_data:
        LANGUAGES.append(row['code'])
        if row['is_default'] == 'Y' or not DEFAULT_LANGUAGE:
            DEFAULT_LANGUAGE = row['code']