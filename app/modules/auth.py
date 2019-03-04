import random
import hashlib
import config

def createSessionID():
    return ''.join([random.choice(config.SESSION_ID_AVAILABLE_CHARACTERS) for _ in range(config.SESSION_ID_SIZE)])

def generateSalt(length=64):
    return ''.join([random.choice(config.SALT_AVAILABLE_CHARACTERS) for _ in range(length)])

def hashPassword(password, salt):
    m = hashlib.sha256(bytes(password, 'utf-8'))
    iteration1 = m.hexdigest()
    m = hashlib.sha256(bytes(iteration1 + config.GLOBAL_SALT, 'utf-8'))
    iteration2 = m.hexdigest()
    m = hashlib.sha256(bytes(iteration2 + salt, 'utf-8'))
    iteration3 = m.hexdigest()
    m = hashlib.sha256(bytes(iteration3 + password, 'utf-8'))
    iteration4 = m.hexdigest()
    return iteration4

def authorization(data, user_data):
    return user_data['password'] == hashPassword(data['password'], user_data['salt'])

def createUIC():
    return ''.join([random.choice(config.UIC_AVAILABLE_CHARACTERS) for _ in range(config.UID_SIZE)])