class iTunesResponse():
    @staticmethod
    def lookup(resp):
        if 'resultCount' not in resp:
            return False

        if resp['resultCount'] == 0:
            return False
        result = resp['results'][0]

        return {
            "name": result['trackName'],
            "bundle_identifier": result['bundleId'],
            "release_date": result['releaseDate'],
            "version": result['version'],
            "identifier": result['trackId'],
            "price": result['price']
        }

    @staticmethod
    def search(resp):
        if 'resultCount' not in resp:
            return False
        items = []
        for result in resp['results']:
            items.append({
                "name": result['trackName'],
                "bundle_identifier": result['bundleId'],
                "release_date": result['releaseDate'],
                "version": result['version'],
                "identifier": result['trackId'],
                "price": result['price']
            })
        return items
