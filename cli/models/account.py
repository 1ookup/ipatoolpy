import json
import os

from cli.logger import logger


class Account:
    def __init__(self, auto_load=True):
        self.name = ""
        self.email = ""
        self.password_token = ""
        self.directory_services_identifier = ""

        user_host = os.path.expanduser('~')
        if not os.path.isdir(f"{user_host}/.config"):
            os.mkdir(f"{user_host}/.config")
        self.config_file = f"{user_host}/.config/ipatool.json"
        if auto_load:
            self.load()

    def __str__(self):
        return f"{self.email} -- {self.name}"

    def to_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_token": self.password_token,
            "directory_services_identifier": self.directory_services_identifier,
        }

    def save(self):
        json.dump(self.to_json(), open(self.config_file, 'w', encoding='utf-8'))

    def load(self):
        if not os.path.isfile(self.config_file):
            logger.warning("ipatool config file is not exist.")
            return False
        try:
            resp = json.load(open(self.config_file, 'r', encoding='utf-8'))
            self.name = resp['name']
            self.email = resp['email']
            self.password_token = resp['password_token']
            self.directory_services_identifier = resp['directory_services_identifier']
            logger.debug("ipatool config load success")
            logger.info(f"Authenticated as {self}")
            return True
        except:
            logger.warning("ipatool config file parse error.")
            return False
