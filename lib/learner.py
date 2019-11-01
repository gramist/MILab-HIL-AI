import os
import csv
import traceback

import pandas as pd
import numpy as np
import time

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras import layers, models
from keras.callbacks import ModelCheckpoint

from lib.processData import Preprocess


class Learner:
    # max = 414
    # C = 1
    # total_acc = 0
    # total_loss = 0
    # count = 0
    def __init__(self, max, C, total_acc, total_loss, count):
        try:
            json_file = open('./model_ae/model%d.json' % C, 'r')
            loaded_ae_json = json_file.read()
            json_file.close()
            ae_model = model_from_json(loaded_ae_json)
            # load weights into new model
            ae_model.load_weights("./model_ae/model%d.h5" % C)
            print("Loaded Autoencoder model from disk")

            ae_model.compile(loss='binary_crossentropy', optimizer='adadelta',
                             metrics=['accuracy'])

            # LSTM Model Load
            json_file = open('./model_lstm/model%d.json' % C, 'r')
            loaded_lstm_json = json_file.read()
            json_file.close()
            lstm_model = model_from_json(loaded_lstm_json)
            # load weights into new model
            lstm_model.load_weights("./model_lstm/model%d.h5" % C)
            print("Loaded LSTM model from disk")

            lstm_model.compile(loss='categorical_crossentropy', optimizer='adam',
                               metrics=['accuracy'])

            process = Preprocess(nor_max=max)

            self.total_acc = total_acc
            self.total_loss = total_loss
            self.count = count
            self.process = process
            self.ae_model = ae_model
            self.lstm_model = lstm_model
            print('Complete Model compile and preprocess')

        except Exception as e:
            print('[Learner-init-ERROR] : ', e)
            traceback.print_exc()

    def getProcess(self):
        return self.process

    def getStatus(self, batch):
        try:
            batch_x = np.array(batch)
            decoded_imgs = self.ae_model.predict(batch_x, verbose=0)
            loss, acc = self.ae_model.evaluate(batch_x, batch_x, verbose=0)
            print("%s: %.2f, %s: %.2f%%" % (self.ae_model.metrics_names[0], loss * 100,
                                            self.ae_model.metrics_names[1], acc * 100))

            self.total_loss += loss
            self.total_acc += acc

            # loss > 3%
            if loss * 100 > 3:
                batch_x = np.reshape(batch_x, (batch_x.shape[0], 1, batch_x.shape[1]))
                y = self.lstm_model.predict(batch_x, verbose=0)
                ans = [np.argmax(i) for i in y]
                print(ans)  # ans == 0: normal , ==1: repeated behavior, ==2: insomnia

                if 1 in ans or 2 in ans:
                    if 1 in ans:
                        status = "Repeated behavior is suspected."
                        return status
                    if 2 in ans:
                        status = "Suspect insomnia"
                        return status
                else:
                    status = "Normal"
                    return status
            else:
                status = 'Normal, loss: {}'.format(loss * 100)
                return status

        except Exception as e:
            print('[Learner-ERROR] : ', e)
            traceback.print_exc()