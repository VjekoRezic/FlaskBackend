from functools import wraps
from flask import Flask
from flask import jsonify

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return {"message":"ADMINS ONLY!!!"}, 403

        return decorator

    return wrapper