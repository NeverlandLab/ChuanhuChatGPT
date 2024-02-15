from loguru import logger
import os
from auth.conf_auth import ConfAuth
from auth.keycloak_auth import KeyCloakAuth

from auth.simple_auth import SimpleAuth
from modules.config import authflag


class AuthBuilder:
    def __init__(self) -> None:
        self.simple_auth = SimpleAuth()
        self.keycloak_auth = KeyCloakAuth()
        self.conf_auth = ConfAuth()

    def build(self):
        if os.getenv("SIMPLE_AUTH_URL") != "":
            logger.info("启用简易用户名/密码认证模式")
            return self.simple_auth.auth
        if os.getenv("KEYCLOAK_AUTH_URL") != "":
            logger.info("启用KeyCloak认证模式")
            return self.keycloak_auth.auth
        elif authflag:
            logger.info("启用配置文件用户名/密码认证模式")
            return self.conf_auth.auth
        else:
            logger.info("没有任何用户认证配置,禁用用户认证校验")
            return None
