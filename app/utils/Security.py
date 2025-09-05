import datetime
import jwt
import os
from dotenv import load_dotenv


class Security():
    load_dotenv()

    # Ahora puedes acceder a las variables de entorno como si estuvieran definidas en el sistema
    token_secret = os.getenv('TOKEN_SECRET')  # TODO: just import them from settings.py

    @classmethod
    def generate_token(cls, email):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=500),
            'email': email
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if ((len(encoded_token) > 0) and (encoded_token.count('.') == 2)):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])

                    # acordarse que con esta mecanica de los roles se puede aplicar
                    # para los roles del aeroclub tengan acceso a ciertos endpoint
                    """
                        roles = list(payload['roles'])

                    if 'Administrator' in roles:
                        return True
                    return False
                    """

                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
        return False

    @classmethod
    def resolvertoken(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if ((len(encoded_token) > 0) and (encoded_token.count('.') == 2)):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])

                    # acordarse que con esta mecanica de los roles se puede aplicar
                    # para los roles del aeroclub tengan acceso a ciertos endpoint
                    """
                        roles = list(payload['roles'])

                    if 'Administrator' in roles:
                        return True
                    return False
                    """

                    return payload
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
        return False
