import traceback

import requests
import json
from operator import eq

from lib.fileIO import FileIO


class requestData:
    def __init__(self):
        self.request_info = FileIO().read_request_info()
        self.url = self.request_info['URL'] + ':' + self.request_info['Port']

    def postData(self, data):
        response = ''
        try:
            packet_type = ''
            if eq(data['PacketType'], 'EstimatedSchedule'):
                packet_type = 'todayschedule'
            elif data['PacketType'] is 'PastSchedule':
                packet_type = 'pastschedule'
            elif data['PacketType'] is 'AbnormalBehavior':
                packet_type = 'abnormalbehavior'
            elif data['PacketType'] is 'OutdoorSensing':
                packet_type = 'outdoorsensing'

            data = json.dumps(data, ensure_ascii=False)
            url = self.url + '/api/ai/' + packet_type
            response = requests.post(url, json=data)

        except Exception as e:
            print('[Request ERROR]\n', e)
            print('[ERROR traceback]\n', traceback.format_exc())
        finally:
            print('postData result : ', response)
            # print(data)
