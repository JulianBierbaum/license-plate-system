from ldap3 import ALL, NTLM, Connection, Server
from src.core.config import settings
from src.exceptions.exceptions import WrongLoginDataException
from src.logger import logger

# install pycryptodome
logger.info(settings.DN)
server = Server(settings.SERVER_IP, get_info=ALL)


def verify_login(username, passwd):
    logger.info(settings.DOMAIN_LOCAL)
    logger.info(settings.DN)
    con = Connection(
        server, user=f"{settings.DN}\\{username}", password=passwd, authentication=NTLM
    )
    if not con.bind():
        con.unbind()
        raise WrongLoginDataException()
    return 1

