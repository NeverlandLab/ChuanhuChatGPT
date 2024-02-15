import logging
import os

import requests


class KeyCloakAuth:
    @staticmethod
    def auth(username, password):
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
            logging.info(f"用户[{username}]登录失败")
            return False
        else:
            logging.info(f"用户[{username}]登录成功")
            return True
