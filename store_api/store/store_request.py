from psutil import net_if_addrs

from cli.logger import logger
from store_api.common.storefront import Storefront
from store_api.store.store_endpoint import StoreEndpoint


class StoreRequest():
    # default guid
    arg_guid = None
    default_guid = "BCD016081FF1"

    def __init__(self, action):
        self.action = action
        self.endpoint = ""
        self.method = "post"
        self.params = None
        self.headers = {
            "User-Agent": "Configurator/2.15 (Macintosh; OS X 11.0.0; 16G29) AppleWebKit/2603.3.8",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.payload = None
        self.payload_type = None

    def guid(self):
        """mac address"""
        if StoreRequest.arg_guid:
            return StoreRequest.arg_guid
        for k, v in net_if_addrs().items():
            if k.startswith('en') or k.startswith('eth'):
                for item in v:
                    if item.family == 18:
                        result = item.address.replace(":", "").upper()
                        return result
        logger.warning("guid use default value.")
        return StoreRequest.default_guid

    @classmethod
    def authenticate(cls, prefix, email, password, code):
        req = StoreRequest("authenticate")
        req.endpoint = StoreEndpoint.authenticate(prefix, req.guid())
        req.headers['Cookie'] = 'itspod=41;'
        req.payload = {
            'appleId': email,
            'attempt': '4' if code else '2',
            "createSession": "true",
            "guid": req.guid(),
            "password": f"{password}{code}" if code else password,
            "rmp": "0",
            "why": "signIn"
        }
        req.payload_type = 'plist'
        return req

    @staticmethod
    def purchase(app_identifier,
                 directory_services_identifier,
                 password_token,
                 country_code):
        req = StoreRequest("purchase")
        req.endpoint = StoreEndpoint.purchase()
        req.headers["X-Dsid"] = str(directory_services_identifier)
        req.headers["iCloud-DSID"] = str(directory_services_identifier)
        req.headers["Content-Type"] = "application/x-apple-plist"
        req.headers["X-Apple-Store-Front"] = Storefront.get(country_code)
        req.headers["X-Token"] = password_token
        req.payload = {
            "appExtVrsId": "0",
            "hasAskedToFulfillPreorder": "true",
            "buyWithoutAuthorization": "true",
            "hasDoneAgeCheck": "true",
            "guid": req.guid(),
            "needDiv": "0",
            "origPage": f"Software-{app_identifier}",
            "origPageLocation": "Buy",
            "price": "0",
            "pricingParameters": "STDQ",
            "productType": "C",
            "salableAdamId": app_identifier
        }
        req.payload_type = "plist"
        return req

    @staticmethod
    def download(app_identifier,
                 directory_services_identifier,
                 external_version_id="", ):
        req = StoreRequest("download")
        req.endpoint = StoreEndpoint.download(req.guid())
        req.headers["X-Dsid"] = directory_services_identifier
        req.headers["iCloud-DSID"] = directory_services_identifier
        req.payload = {
            "creditDisplay": "",
            "guid": req.guid(),
            "salableAdamId": str(app_identifier),
        }
        if external_version_id:
            req.payload['externalVersionId'] = str(external_version_id)
        req.payload_type = "plist"
        return req
