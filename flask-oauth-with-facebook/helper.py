from functools import wraps
from flask import redirect, session, url_for

import settings




"""
The goal is to limit transport of the facebook token. If we
have the api token compromised, there's a better chance to 
do some damage control on the server side.

1. check the api token. if DNE, goto 2.
2. check that fb token. cross check it with provided name/email.

Another option is to investigate use of flask-security.
We just want to avoid session based systems. This API must be
stateless. Token authentication looks probable.
"""
def authenticated(f):
    """ 
    Checks if user is logged in .
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('api_token'):
            if not session.get('facebook_token'):
                return redirect(url_for('index'))
            #else:
                # create an api token here?
                
        return f(*args, **kwargs)
    return decorated


