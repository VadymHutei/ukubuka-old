app_config = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 80
}

db_params = {
    'host': 'ukubuka.net',
    'user': 'root',
    'password': 'root',
    'db': 'ukubuka',
    'charset': 'utf8mb4'
}
db_prefix = 'ku_'

site_name = 'Ukubuka'

languages = ('ukr', 'eng')
default_language = 'ukr'

# RE_RAW_PHONE              r'[0-9\s-\(\)\+]{7,20}'
# RE_RAW_FULL_PHONE         r'\+380 \([0-9]{2}\) [0-9]{3}-[0-9]{2}-[0-9]{2}'
# RE_RAW_FULL_PHONE_MASK    r'\+380 \([0-9_]{2}\) [0-9_]{3}-[0-9_]{2}-[0-9_]{2}'

# RE_FULL_PHONE             r'/^\+380 \([0-9]{2}\) [0-9]{3}-[0-9]{2}-[0-9]{2}$/'
# RE_COMMON_PHONE           r'/^[\+\-\(\) 0-9]{9,20}$/'
# RE_NUMBERS                r'/[0-9]/'
# RE_LETTERS                r'/[a-zA-Zа-яА-ЯіІїЇєЄґҐ]/'
# RE_KG_USER                r'/^[a-zA-Z0-9]{32}$/'
# RE_USER_ID                r'/^[0-9]{1,8}$/'
# RE_EMAIL                  r'/^[a-zA-Z0-9\.\-_]+@[a-zA-Z0-9\.\-_]+$/'
# RE_USER_NAME              r'/^[a-zA-Zа-яА-ЯіІїЇєЄґҐ]{2,64}$/u'
# RE_CALLBACK_NAME          r'/^[ \-_0-9a-zA-Zа-яА-ЯіІїЇєЄґҐ]{2,128}$/u'
# RE_PASSWORD               r'/^[0-9A-Za-z !"#\$%&\'\(\)\*\+,-\.\/\\:;<=>\?@\[\]\^_`\{\|\}~]{3,64}$/'