import os
import traceback

import numpy as np
from tensorflow.keras.models import model_from_json

from lib.processData import Preprocess


class Learner:
    # max_val = 414
    # C = 1
    # total_acc = 0
    # total_loss = 0
    # count = 0
    def __init__(self, max_val, C, total_acc, total_loss, count):
        try:
            process = Preprocess(nor_max=max_val)
            print(os.getcwd())
            # Autoencoder Model load
            json_file = open('./model_ae/model%d.json' % C, 'r')
            loaded_ae_json = json_file.read()
            json_file.close()
            ae_model = model_from_json(loaded_ae_json)
            # load weights into new model
            ae_model.load_weights("./model_ae/model%d.h5" % C)
            print("Loaded Autoencoder model from disk")

            ae_model.compile(loss='binary_crossentropy', optimizer='adam',
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

            # # # Vae Model load
            # json_file = open('./model_vae/model%d.json' % C, 'r')
            # loaded_vae_json = json_file.read()
            # json_file.close()
            # vae_model = model_from_json(loaded_vae_json)
            # # load weights into new model
            # vae_model.load_weights("./model_vae/model%d.h5" % C)
            # print("Loaded Vae model from disk")
            #
            # vae_model.compile(loss='binary_crossentropy', optimizer='adadelta',
            #                   metrics=['accuracy'])

            self.total_acc = total_acc
            self.total_loss = total_loss

            self.count = count
            self.process = process

            self.ae_model = ae_model
            self.lstm_model = lstm_model
            self.vae_model = vae_model

            self.max = max_val
            print('Complete Models compile and preprocess')

        except Exception as e:
            print('[Learner-init-ERROR] : ', e)
            traceback.print_exc()

    def getProcess(self):
        return self.process

    def getStatus(self, batch):
        try:
            batch_x = np.array(batch)
            # decoded_imgs = self.ae_model.predict(batch_x, verbose=0)
            self.ae_model.predict(batch_x, verbose=0)
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
                        status = "반복행동이 의심됩니다."
                        return status
                    if 2 in ans:
                        status = "불면증세를 보입니다."
                        return status
                else:
                    # status = "Normal"
                    return False
            else:
                # status = 'Normal, loss: {}'.format(loss * 100)
                return False

        except Exception as e:
            print('[Learner-ERROR] : ', e)
            traceback.print_exc()

    def decodeData(self, data_):
        decoded = []
        data_ = data_.tolist()
        for i, data in enumerate(data_):
            h = np.argmax(data[:24])+1
            m = (np.argmax(data[24:30])+1) * 10
            if 60 == m:
                h += 1
                if 24 <= h:
                    h = 0
                m = 00
            s = np.argmax(data[30:36])+1

            nor = data[36] * self.max
            # nor = data[36] * std_max

            decoded.append([h, m, s, int(nor)])

        return decoded

    def make_schedule(self, batch):
        # print('batch : ', batch)
        batch_x = np.array(batch)
        batch_x = np.reshape(batch_x, (96,))
        decoded_imgs = self.vae_model.predict(batch_x, verbose=0)
        # print(decoded_imgs)
        loss, acc = self.vae_model.evaluate(batch_x, batch_x, verbose=0)
        print("%s: %.2f, %s: %.2f%%" % (self.vae_model.metrics_names[0], loss * 100,
                                        self.vae_model.metrics_names[1], acc * 100))

        newData = self.decodeData(decoded_imgs)

        return newData
