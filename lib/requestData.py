import requests
from lib.fileIO import FileIO


class requestData:
    def __init__(self):
        request_info = FileIO().read_request_info()
        self.url = request_info['URL'] + request_info['Port']

    def postData(self, data):
        try:
            response = requests.post(self.url, data=data)
        except Exception as e:
            print('[Request ERROR]\n' + e)
        finally:
            print('postData result : ', response)

