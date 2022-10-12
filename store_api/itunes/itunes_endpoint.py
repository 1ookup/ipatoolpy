class iTunesEndpoint:
    scheme = "https"
    host = "itunes.apple.com"

    @staticmethod
    def search():
        path = "/search"
        url = f"{iTunesEndpoint.scheme}://{iTunesEndpoint.host}{path}"
        return url

    @staticmethod
    def lookup():
        path = "/lookup"
        url = f"{iTunesEndpoint.scheme}://{iTunesEndpoint.host}{path}"
        return url
