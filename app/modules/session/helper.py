import random
import re
import config

def create_session_id():
    return ''.join([random.choice(config.session_id_available_characters) for _ in range(64)])

def validSessionId(session_id):
    if isinstance(session_id, str):
        return bool(re.fullmatch(r'[0-9a-z]{64}', session_id))
    return False