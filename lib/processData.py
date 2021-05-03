import os
import datetime

import numpy as np
from pandas import DataFrame

from lib import controller


def after_process(schedule_list):

    after_list = []
    for row in schedule_list:
        split_data = row.split(', ')

        time_str = '2019-01-01 ' + split_data[0] + ':00'
        row_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        times = [
            '2019-01-01 06:00:00',
            '2019-01-01 07:00:00',
            '2019-01-01 07:20:00',
            '2019-01-01 08:30:00',
            '2019-01-01 10:00:00',
            '2019-01-01 12:30:00',
            '2019-01-01 13:30:00',
            '2019-01-01 17:00:00',
            '2019-01-01 18:30:00',
            '2019-01-01 20:00:00',
            '2019-01-01 22:00:00'
        ]

        for i, val in enumerate(times):
            times[i] = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')

        if times[0] <= row_time <= times[1]:
            if (split_data[1] == '방문 열림') or (split_data[1] == '화장실 이용'):
                after_list.append(['06:00~07:00', '기상'])
        elif times[2] <= row_time <= times[3]:
            if (split_data[1] == '냉장고 이용') or (split_data[1] == '식사 시간') or (split_data[1] == '화장실 이용'):
                after_list.append(['07:00~08:30', '아침식사,위생관리'])
        elif times[3] <= row_time <= times[4]:
            if (split_data[1] == '방문 열림') or (split_data[1] == '화장실 이용'):
                after_list.append(['08:30~10:00', '건강체크,물리치료'])
        elif times[4] <= row_time <= times[5]:
            if (split_data[1] == '외출 시간') or (split_data[1] == '방문 열림'):
                after_list.append(['10:00~12:30', '휴식 및 여가활동'])
        elif times[5] <= row_time <= times[6]:
            if (split_data[1] == '화장실 이용') or (split_data[1] == '냉장고 이용') or \
                    (split_data[1] == '식사 시간') or (split_data[1] == '약 복용 시간'):
                after_list.append(['12:30~13:30', '점심식사,위생관리,투약'])
        elif times[6] <= row_time <= times[7]:
            if (split_data[1] == '외출 시간') or (split_data[1] == '방문 열림'):
                after_list.append(['13:30~17:00', '산책 및 휴식'])
        elif times[7] <= row_time <= times[8]:
            if (split_data[1] == '화장실 이용') or (split_data[1] == '냉장고 이용') or \
                    (split_data[1] == '식사 시간') or (split_data[1] == '약 복용 시간'):
                after_list.append(['17:00~18:30', '저녁식사,위생관리,투약'])
        elif times[8] <= row_time <= times[9]:
            if (split_data[1] == '외출 시간') or (split_data[1] == '방문 열림'):
                after_list.append(['18:30~20:00', '휴식 및 여가활동'])
        elif times[9] <= row_time <= times[10]:
            if (split_data[1] == '방문 열림') or (split_data[1] == '화장실 이용'):
                after_list.append(['20:00~22:00', '수면환경 점검'])

    tmp = np.array(after_list)
    after_list = DataFrame(tmp).drop_duplicates().values

    return after_list


class Preprocess:
    def __init__(self, dir_=None, data_=None, option_=1, len_=0, sum_=0,
                 nor_max=0, nor_min=1):
        self.hour = 24
        self.minute = 6
        self.nSensor = 11
        self.nLabel = 3

        self.data_len = len_
        self.hash_sum = sum_
        self.hash_mean = 0
        self.hash_stddev = 0
        self.max = nor_max
        self.min = nor_min

        self.dir = dir_
        self.data = data_
        # print(self.data)

        self.option = option_

        if dir_:
            self.inputDir = dir_ + 'input/'
            if not os.path.isdir(self.inputDir):
                os.mkdir(self.inputDir)

        # self.main()

    def num2onehot(self, nCate, n):
        onehot = []
        for i in range(nCate):
            onehot.append(0)
        onehot[int(n) - 1] = 1
        return onehot

    def normalization(self, hashs):
        tmpMax = max(hashs)

        self.max = max(tmpMax, self.max)

    def log2onehot(self, log):

        h, m, _ = log[1].split(':')
        m = int(m) // 10 + 1

        newData = self.num2onehot(self.hour, h)  # [0:24]
        newData += self.num2onehot(self.minute, m)  # [24:30]
        newData += self.num2onehot(self.nSensor, log[2])  # [30:35]

        # when standardization
        # z_score = (log[3] - self.hash_mean) / self.hash_stddev
        # newData.append(z_score)   # [35]

        # normalization
        norm = (log[3] - self.min) / (self.max - self.min)
        newData.append(norm)  # [35]

        if self.option == 2:
            newData += self.num2onehot(self.nLabel, log[4] + 1)

        return newData

    def process(self, patient_seq):
        get_data = controller.get_sensor_list(patient_seq)
        cnt_list = controller.get_sensor_cnt_list(get_data)

        self.normalization(cnt_list)

        result_list = []
        for i, log in enumerate(get_data):
            log[2] = int(log[2])
            log[3] = int(log[3])
            newData = self.log2onehot(log)
            result_list.append(newData)

        return result_list
