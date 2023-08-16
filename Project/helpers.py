from flask import redirect, session
from functools import wraps

def login_required(f):
    """Decorate routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function

def sulogin_required(f):
    """Decorate superuser routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("su_id") is None:
            return redirect("/sulogin")
        return f(*args, **kwargs)
    
    return decorated_function