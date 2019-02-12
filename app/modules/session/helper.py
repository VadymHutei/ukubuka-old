import modules.validation as validation

def prepareAuthenticationFormData(form):
    result = {}
    email = form.get('email')
    password = form.get('password')
    if email: result['email'] = email
    if password: result['password'] = password
    return result

def validAuthenticationData(data):
    if 'email' not in data or not validation.email(data['email']): return False
    if 'password' not in data or not validation.password(data['password']): return False
    return True