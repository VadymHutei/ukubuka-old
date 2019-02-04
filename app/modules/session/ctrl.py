import config
import modules.session.model as model
import modules.session.helper as helper

class Session():

    def __init__(self, session_id, **kwargs):
        self.id = session_id
        self.remote_address = kwargs.get('remote_address')

    def isValid(self):
        if self.id is None: return False
        if helper.validSessionId(self.id):
            return model.sessionExist(self.id)
        return False

    def start(self):
        for x in range(config.session_id_generation_attempts):
            session_id = helper.create_session_id()
            if not model.sessionExist(session_id):
                self.id = session_id
                model.createSession(self.id)
                return self.id
        return False

    def increaseVisits(self):
        model.increaseVisits(self.id, self.remote_address)