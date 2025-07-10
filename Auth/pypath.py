from ldap3 import *#Server, Connection, ALL, NTLM, SUBTREE, BASE, LEVEL
import os
from dotenv import load_dotenv
import json


# get data from ..env
load_dotenv()

DOMAIN_NAME = os.getenv('DOMAIN_NAME') #eg.: name
DOMAIN_LOCAL = os.getenv('DOMAIN_LOCAL') #eg.: at
DOMAIN = f"{DOMAIN_NAME}.{DOMAIN_LOCAL}" #DN: Domain name, eg.: name.at
ROOT_DN = f"dc={DOMAIN_NAME},dc={DOMAIN_LOCAL}"
AD_SERVER = os.getenv('SERVER') #eg.: 173.12.7.2
AD_USERNAME = os.getenv('AD_USERNAME') #eg.: mustermann1
PASSWORD = os.getenv('PASSWORD') #eg.: Kennwort1
SECRET_KEY = os.getenv('S_KEY')

server = Server(AD_SERVER, get_info=ALL)

def verify_login(username, passwd):
    # print(f"{DOMAIN}\\{username}")
    con=Connection(server,user=f"{DOMAIN}\\{username}", password=passwd, authentication=NTLM)
    if not con.bind():
        con.unbind()
        return 0
    else:
        con.unbind()
        return 1
