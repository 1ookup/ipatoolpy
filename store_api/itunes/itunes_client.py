from networking.http_client import HTTPClient
from store_api.itunes.itunes_endpoint import iTunesEndpoint
from store_api.itunes.itunes_response import iTunesResponse


class iTunesClient:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def search(self, term, limit, country_code, device_family):
        endpoint = iTunesEndpoint.search()
        params = {
            "media": "software",
            "term": term,
            "limit": str(limit),
            "country": country_code,
            "entity": DeviceFamily.entity(device_family)
        }
        resp = self.http_client.get(endpoint, params=params)
        decoded = iTunesResponse.search(resp.json())
        return decoded

    def lookup(self, bundle_identifier, country_code, device_family):
        endpoint = iTunesEndpoint.lookup()
        params = {
            "media": "software",
            "bundleId": bundle_identifier,
            "limit": "1",
            "country": country_code,
            "entity": DeviceFamily.entity(device_family)
        }
        resp = self.http_client.get(endpoint, params=params)
        decoded = iTunesResponse.lookup(resp.json())
        return decoded


class DeviceFamily():
    @staticmethod
    def entity(device):
        if device == 'pad':
            return "iPadSoftware"
        elif device == 'phone':
            return "software"
        else:
            return "software"
