import os
import csv
import pandas as pd


class Preprocess:
    def __init__(self, dir_=None, data_=None, option_=1, len_=0, sum_=0,
                 nor_max=0, nor_min=1):
        self.hour = 24
        self.minute = 6
        self.nSensor = 7
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
