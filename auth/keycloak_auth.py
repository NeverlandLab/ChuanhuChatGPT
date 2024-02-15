from loguru import logger
import os

import requests


class KeyCloakAuth:

    def auth(self, username, password):
        data = {
            "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
            "username": username,
            "password": password,
            "grant_type": "password",
        }

        response = requests.post(os.getenv("KEYCLOAK_AUTH_URL"), data=data)
        response.raise_for_status()
        token = response.json().get("access_token")
        if token is None:
            logger.info(f"用户[{username}]登录失败")
            return False
        else:
            logger.info(f"用户[{username}]登录成功")
            return True
