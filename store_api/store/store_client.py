import plistlib

from cli.logger import logger
from cli.models.account import Account
from networking.http_client import HTTPClient
from store_api.store.store_request import StoreRequest
from store_api.store.store_response import StoreResponse


class StoreClient():
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def get_header(self):
        return {
            "User-Agent": "Configurator/2.15 (Macintosh; OS X 11.0.0; 16G29) AppleWebKit/2603.3.8",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def authenticate(self, email, password, code=None, is_first_attempt=True):
        prefix = "p25" if code == None else "p71"
        request = StoreRequest.authenticate(prefix,
                                            email,
                                            password,
                                            code)
        resp = self.http_client.send(request)
        if request.payload_type == 'plist':
            resp = plistlib.loads(resp.content)
        decoded = StoreResponse.authenticate(resp)
        if decoded:
            account = Account(auto_load=False)
            first_name = decoded['first_name']
            last_name = decoded['last_name']
            directory_services_identifier = decoded['directory_services_identifier']
            account.password_token = decoded['password_token']
            account.email = email
            account.directory_services_identifier = directory_services_identifier
            account.name = f"{first_name} {last_name}"
            account.save()
            self.http_client.save_cookie()
            return account
        else:
            if code:
                return False
            code = input("Enter 2FA code: ").strip()
            self.authenticate(email, password, code)

    def purchase(self, identifier,
                 directory_services_identifier,
                 password_token,
                 country_code):
        logger.info(f"Obtaining a license for '{identifier}' from the App Store...")
        request = StoreRequest.purchase(identifier,
                                        directory_services_identifier,
                                        password_token,
                                        country_code)
        resp = self.http_client.send(request)
        if resp.status_code == 500:
            logger.warning("A license already exists for this item.")
            return False
        else:
            if request.payload_type == 'plist':
                resp = plistlib.loads(resp.content)
            decoded = StoreResponse.purchase(resp)
            return decoded

    def item(self, identifier, directory_services_identifier, external_version_id=""):
        request = StoreRequest.download(identifier, directory_services_identifier, external_version_id)
        resp = self.http_client.send(request)
        if request.payload_type == 'plist':
            resp = plistlib.loads(resp.content)
        decoded = StoreResponse.item(resp)
        return decoded
