import requests
import json

from lib.fileIO import FileIO


class requestData:
    def __init__(self):
        self.request_info = FileIO().read_request_info()
        self.url = self.request_info['URL'] + self.request_info['Port']

    def postData(self, data):
        try:
            packet_type = ''
            if data['PacketType'] == 'EstimatedSchedule':
                packet_type = 'todayschedule'
            elif data['PacketType'] == 'PastSchedule':
                packet_type = 'pastschedule'
            elif data['PacketType'] == 'AbnormalBehavior':
                packet_type = 'abnormalbehavior'
            elif data['PacketType'] == 'OutdoorSensing':
                packet_type = 'outdoorsensing'

            url = self.url + '/api/ai/' + packet_type
            response = requests.post(url, json=data)

        except Exception as e:
            print('[Request ERROR]\n', e)
        finally:
            print('postData result : ', response.status_code)