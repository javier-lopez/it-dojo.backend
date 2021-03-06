from threading import Thread
from functools import wraps
from flask     import request, jsonify

from config    import Config

def threaded(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def check_auth(username, password):
    return username == 'key' and password == Config.API_KEY

def authenticate():
    message = {
        'message': "Requires Authentication",
        'status': 401,
    }
    return jsonify(message), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
