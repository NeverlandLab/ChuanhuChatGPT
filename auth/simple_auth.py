import os
import requests


class SimpleAuth:
    def auth(username, password):
        data = {
            "username": username,
            "password": password,
        }
        response = requests.post(os.getenv("SIMPLE_AUTH_URL"), data=data)
        response.raise_for_status()
        result = response.json().get("success")
        return result
