class StoreResponse():
    @staticmethod
    def purchase(resp):
        if 'status' in resp and 'jingleDocType' in resp:
            if resp['status'] == 0 and resp['jingleDocType'] == 'purchaseSuccess':
                return True
        return False

    @staticmethod
    def item(resp):
        if 'status' in resp and 'jingleDocType' in resp:
            if resp['status'] == 0 and resp['jingleDocType'] == 'purchaseSuccess':
                result = resp['songList'][0]
                return result
        return False

    @staticmethod
    def authenticate(resp):
        if 'passwordToken' in resp:
            result = {
                "first_name": resp['accountInfo']['address']['firstName'],
                "last_name": resp['accountInfo']['address']['lastName'],
                "directory_services_identifier": resp['dsPersonId'],
                "password_token": resp['passwordToken']
            }
            return result
        return False
