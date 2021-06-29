import keras
from keras.models import Sequential
from keras.layers import Input, Lambda, Dense, LSTM, Dropout, BatchNormalization, Activation
from keras.models import model_from_json, Model
from keras import layers, models, optimizers
from keras.callbacks import ModelCheckpoint
from keras import backend as K

import tensorflow as tf


def Autoencoder(input=96, z_dim=16):
    model = Sequential()
    encoder = model.add(Dense(z_dim, input_dim=input, kernel_initializer='uniform', activation='relu'))
    model.add(Dropout(0.2))
    decoder = model.add(Dense(input, kernel_initializer='uniform', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())

    return model


def LSTM_A(input=96, step=1, hidden=36):
    model = Sequential()
    # model.add(LSTM(hidden, input_dim=input, return_sequences=True))
    model.add(LSTM(hidden, input_shape=(step, input), return_sequences=True))
    model.add(Dropout(0.2))
    # model.add(LSTM(hidden, return_sequences=False))
    # model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())

    return model


def sampling(args):
    """Reparameterization trick by sampling from an isotropic unit Gaussian.
    # Arguments
        args (tensor): mean and log of variance of Q(z|X)
    # Returns
        z (tensor): sampled latent vector
    """
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    # by default, random_normal has mean = 0 and std = 1.0
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon


def VariationalAE(input=96, hidden=16, latent_dim=8):
    '''
    model = Sequential()
    model.add(Dense(hidden, input_dim=input, kernel_initializer='uniform', acrtivation='relu', name='encoder_input'))
    '''
    # z_log_var = model.add(Dense(latent_dim, name='z_log_var'))

    inputs = Input(shape=(input,), name='encoder_input')
    x = Dense(hidden, activation='relu')(inputs)
    z_mean = Dense(latent_dim, name='z_mean')(x)
    z_log_var = Dense(latent_dim, name='z_log_var')(x)

    # use reparameterization trick to push the sampling out as input
    # note that "output_shape" isn't necessary with the TensorFlow backend
    z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

    # instantiate encoder model
    encoder = Model(inputs, [z_mean, z_log_var, z], name='encoder')
    encoder.summary()
    # plot_model(encoder, to_file='vae_mlp_encoder.png', show_shapes=True)

    # build decoder model
    latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
    x = Dense(hidden, activation='relu')(latent_inputs)
    outputs = Dense(input, activation='sigmoid')(x)

    # instantiate decoder model
    decoder = Model(latent_inputs, outputs, name='decoder')
    decoder.summary()
    # plot_model(decoder, to_file='vae_mlp_decoder.png', show_shapes=True)

    # instantiate VAE model
    outputs = decoder(encoder(inputs)[2])
    model = Model(inputs, outputs, name='vae_mlp')
    model.compile(loss='binary_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    print(model.summary())

    return model

'''
def LSTM_(X_, n_input = 36, n_step = 1, n_hidden = 32, n_class = 3):

    n_input = 36
    n_step = 1
    n_hidden = 32
    n_class = 3

    X = tf.placeholder(tf.float32, [None, n_step, n_input])
    Y = tf.placeholder(tf.float32, [None, n_class])

    with tf.name_scope('layer1'):
        W = tf.Variable(tf.random_normal([n_hidden, n_class]), name='W1')
        b = tf.Variable(tf.random_normal([n_class]))

    # cell = tf.nn.rnn_cell.BasicRNNCell(n_hidden)
    cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden)

    outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

    outputs = tf.transpose(outputs, [1, 0, 2])
    outputs = outputs[-1]


    model = tf.matmul(outputs, W) + b

    return model
'''
