import jwt
import datetime
from pypath import verify_login, SECRET_KEY


algorithm = 'HS256'

def authenticate_token(token):
    """verify the credibility of a token

    Args:
        token (string): Your JWT

    Returns:
        0: Token not credible
        str: Token credible, returns new Token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        exp = payload['exp']
        if exp<=0:
            print("Token expired, you need to log in again.")
            return 0
        else:
            password = payload['password']
            username = payload['username']
            return authenticate(username, password)
    except Exception as e:
        print("Token not credible")
        return 0


def authenticate(username, password):
    """verify username and password

    Args:
        username (string): username of AD user (only username, no special domain formatting)
        password (string): plain text password of user username

    Returns:
        0: wrong credentials entered
        1: right credentials entered
    """
    result = verify_login(username, password)
    return result
    


def new_token(username:str, password:str):
    """create a new JWT using username and password

    Args:
        username (str): username of AD user (only username, no special domain formatting)
        password (str): plain text password of user username

    Returns:
        0: input not credible
        str: credible input, returns new token
    """
    if authenticate(username, password) == 0:
        return 0
    else:
        payload = {
            'username': username,
            'password': password,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Expires in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm)
        return token

# Tests
# print(authenticate_token("jahsdfasdfasdf"))    
# print(authenticate("ADSync.Trainee", "QqfJkHjxGgxTQNJ6ap"))
# print(new_token("ADSync.Trainee", "QqfJkHjxGgxTQNJ6ap"))
# print(authenticate_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFEU3luYy5UcmFpbmVlIiwicGFzc3dvcmQiOiJRcWZKa0hqeEdneFRRTko2YXAiLCJleHAiOjE3NTIwNzkxNzl9.XmKVTXdXNb1wtDvY7Ro5ZHNPAlKEct1JpjTeNP3cTeU"))
