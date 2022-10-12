import os.path
import pickle
import plistlib

import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class HTTPClient():
    proxy = None

    def __init__(self):
        self.session = requests.session()
        self.__load_cookie()

    def get(self, url, **kwargs):
        if HTTPClient.proxy:
            kwargs['verify'] = False
            kwargs['proxies'] = {
                "https": HTTPClient.proxy
            }
        return self.session.get(url=url, **kwargs)

    def __load_cookie(self):
        user_home = os.path.expanduser("~")
        config_path = os.path.join(user_home, '.config')
        if not os.path.isdir(config_path):
            os.mkdir(config_path)
        self.cookie_file = os.path.join(config_path, 'ipatool.cookie')
        if not os.path.isfile(self.cookie_file):
            return False
        with open(self.cookie_file, 'rb') as f:
            self.session.cookies.update(pickle.load(f))
        return True

    def save_cookie(self):
        with open(self.cookie_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def send(self, request, **kwargs):
        if HTTPClient.proxy:
            kwargs['verify'] = False
            kwargs['proxies'] = kwargs['proxies'] = {
                "https": HTTPClient.proxy
            }
        url = request.endpoint
        method = request.method
        headers = request.headers
        params = request.params
        payload = None
        if request.payload_type == 'plist':
            payload = plistlib.dumps(request.payload)
        return self.session.request(method=method,
                                    url=url,
                                    params=params,
                                    headers=headers,
                                    data=payload,
                                    **kwargs)
