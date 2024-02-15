import json


class ConfAuth:
    @staticmethod
    def auth(username, password):
        try:
            with open("config.json", encoding="utf-8") as f:
                conf = json.load(f)
            usernames, passwords = [i[0] for i in conf["users"]], [
                i[1] for i in conf["users"]
            ]
            if username in usernames:
                if passwords[usernames.index(username)] == password:
                    return True
            return False
        except:
            return False
