import requests
from lib.fileIO import FileIO


class requestData:
    def __init__(self):
        request_info = FileIO().read_request_info()
        self.url = request_info['URL'] + request_info['Port']

    def postData(self, data):
        try:
            # 완성되면 이 부분의 주석을 풀어서 HIL 서버로 request를 날려. print 부분은 지워버리고....
            response = requests.post(self.url, data=data)
            # response = data
        except Exception as e:
            print('[Request ERROR]\n', e)
        finally:
            print('postData result : ', response)
