import datetime
import config
import modules.session.model as model
import modules.session.helper as helper
import modules.lib.validation as validation
import modules.lib.auth as auth

class Session():

    def __init__(self, session_id, **kwargs):
        self.id = session_id
        self.uic = kwargs.get('uic')
        self.remote_address = kwargs.get('remote_address')
        self.user = {}

    def isValid(self):
        if self.id is None: return False
        if validation.sessionId(self.id):
            return model.sessionExist(self.id)
        return False

    def isAuth(self):
        if self.uic is None: return False
        uic_expired = model.getUICExpired(self.uic)
        if not uic_expired: return False
        return datetime.datetime.now() < uic_expired

    def authorization(self, level):
        if not self.isAuth(): return False
        if level == 'admin':
            self.user['id'] = model.getUserIdByUIC(self.uic)
            self.user['group'] = model.getUserGroup(self.user['id'])
            print(self.user)
            return level == self.user['group']
        return True

    def start(self):
        for x in range(config.SESSION_ID_GENERATION_ATTEMPTS):
            session_id = auth.createSessionID()
            if not model.sessionExist(session_id):
                self.id = session_id
                model.createSession(self.id)
                return self.id
        return False

    def increaseVisits(self):
        model.increaseVisits(self.id, self.remote_address)

    def authentication(self, form):
        data = helper.prepareAuthenticationFormData(form)
        if not helper.validAuthenticationData(data): return False
        user_id = model.getUserIdByEmail(data['email'])
        if not user_id: return False
        user_data = model.getUserAuthenticationData(user_id)
        if not user_data: return False
        if not auth.authorization(data, user_data): return False
        uic = auth.createUIC()
        current_date = datetime.datetime.now()
        expire_date = current_date + datetime.timedelta(days=config.UIC_EXPIRES)
        model.setUIC(uic, user_id, current_date, expire_date)
        return uic, expire_date