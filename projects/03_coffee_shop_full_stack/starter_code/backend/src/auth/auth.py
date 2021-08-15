import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-sitffinx.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drinks'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    """
    Get token from authorization header and raise error is header is incorrect.
    :return:
    """
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise AuthError({
            'success': False,
            'message': 'Unauthorized',
            'error': 401
        }, 401)

    authorization_parts = authorization.split(' ')
    if authorization_parts[0].lower() != 'bearer':
        raise AuthError({
            'success': False,
            'message': 'Missing bearer',
            'error': 401
        }, 401)

    elif len(authorization_parts) == 1:
        raise AuthError({
            'success': False,
            'message': 'Missing token',
            'error': 401
        }, 401)

    elif len(authorization_parts) > 2:
        raise AuthError({
            'success': False,
            'message': 'Missing token',
            'error': 401
        }, 401)

    token = authorization_parts[1]
    return token


def check_permissions(permission, payload):
    """
        Check permission against a payload.
        :param permission:
        :param payload:
        :return:
        """
    if 'permissions' in payload and permission in payload['permissions']:
        return True

    raise AuthError({
        'success': False,
        'error': 403,
        'message': 'Un authorized'
    }, 403)


def verify_decode_jwt(token):
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'message': 'Invalid token',
            'error': 401
        }, 401)

    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'message': 'Token expired',
                'error': 401
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'message': 'Invalid token',
                'error': 401
            }, 401)

        except Exception:
            raise AuthError({
                'success': False,
                'message': 'Unable to parse',
                'error': 400
            }, 400)

    raise AuthError({
        'success': False,
        'message': 'Invalid key',
        'error': 400
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
