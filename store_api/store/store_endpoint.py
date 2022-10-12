class StoreEndpoint():
    scheme = "https"

    @staticmethod
    def authenticate(prefix, guid):
        host = f"{prefix}-buy.itunes.apple.com"
        path = f"/WebObjects/MZFinance.woa/wa/authenticate?guid={guid}"
        return f"{StoreEndpoint.scheme}://{host}{path}"

    @staticmethod
    def download(guid):
        host = "p25-buy.itunes.apple.com"
        path = f"/WebObjects/MZFinance.woa/wa/volumeStoreDownloadProduct?guid={guid}"
        return f"{StoreEndpoint.scheme}://{host}{path}"

    @staticmethod
    def purchase():
        host = "buy.itunes.apple.com"
        path = "/WebObjects/MZBuy.woa/wa/buyProduct"
        return f"{StoreEndpoint.scheme}://{host}{path}"
