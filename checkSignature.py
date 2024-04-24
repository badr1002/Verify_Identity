# handle check token if expired using jwt and signature
import jwt
from decouple import config


def decode_token(token):
    try:
        # decode token
        new_token = token.split(" ")[1]
        decoded = jwt.decode(new_token, verify=False, algorithms=['HS256'], key=config('JWT_KEY'))
        if (not decoded.get("is_superuser", False)):
            raise Exception('Unauthorized', 401)
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired', 401)
    except jwt.InvalidTokenError:
         raise Exception('Invalid token', 401)
    except Exception as e:
        raise Exception(e.args[0], e.args[1] if len(e.args) > 1 else 500)

        
 