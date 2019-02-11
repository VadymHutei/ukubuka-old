app_config = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 80
}

site_name = 'My Site'

session_cookie_name = 'sessid'
session_cookie_expires = 90 # days
session_id_available_characters = '0123456789abcdefghijklmnopqrstuvwxyz'
session_id_generation_attempts = 10

db_params = {
    'host': 'localhost',
    'user': 'user_name',
    'password': 'password',
    'db': 'db_name',
    'charset': 'utf8mb4'
}
db_prefix = 'prfx_'

languages = ('ukr', 'eng')
default_language = 'ukr'

GLOBAL_SALT = 'GLOBAL_SALT'