import config
import modules.session.model as model
import modules.session.helper as helper

class Session():

    def __init__(self):
        pass

    def start(self):
        for x in range(config.session_id_generation_attempts):
            session_id = helper.create_session_id()
            if model.is_available(session_id):
                model.create_session(session_id)
                return session_id
        return False