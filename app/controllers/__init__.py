from flask import *
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

def auth_required(f):
    '''Decorator to require a valid token
        Token must be present in authorization header
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app = current_app._get_current_object()
        token = request.headers.get("authorization")

        if verify_auth_token(app, token):
            return f(*args, **kwargs)
        else:
            return get_error_response("Unauthorized")
    return decorated_function

def verify_auth_token(app, token):
    """Verify that the presented token is Valid"""
    s = Serializer(app.config['SECRET_KEY'])
    if token is not None:
        try:
            print "THIS IS THE TOKEN {token}".format(token=token)
            data = s.loads(token)
        except SignatureExpired:
            return False #Valid token but expired
        except BadSignature:
            return False # invalid token
        return True
    else:
        return False


def get_success_response(results={}):
    """Format the success JSON response object"""
    results["success"] = True
    return jsonify(results)

def get_error_response(message):
    """"Format the error JSON response object"""
    response = jsonify({
        "success": False,
        "error": message
    })
    return response