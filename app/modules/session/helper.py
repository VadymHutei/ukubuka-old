import random
import config

def create_session_id():
    return ''.join([random.choice(config.session_id_available_characters) for _ in range(64)])