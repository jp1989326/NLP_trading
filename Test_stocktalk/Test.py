def cnn_133(train, train_vali, epoch_no = 5, encoder_dim=[100, 100, 100], decoder_dim=[100, 100, 100]):
    
    # CNN autoencoder
   
    #batch_size = 100
    start = timeit.default_timer()
    x = Input(shape=(666,1 ))
    h = Convolution1D(9, 9, activation = 'relu', name='conv_1')(x)
    h = Flatten(name='flatten_1')(h)
    h = Dense(encoder_dim[2], activation = 'relu', name='dense_1')(h)
    
    
    z_mean = Dense(encoder_dim[2])(h)
    z_log_var = Dense(encoder_dim[2])(h)


    def sampling(args):
        z_mean, z_log_var = args
        epsilon = K.random_normal(shape=(encoder_dim[2], ), mean=0.)
        return z_mean + K.exp(z_log_var / 2) * epsilon

    # note that "output_shape" isn't necessary with the TensorFlow backend
    z = Lambda(sampling, output_shape=(encoder_dim[2],))([z_mean, z_log_var])

    # we instantiate these layers separately so as to reuse them later
    decoder_h = Dense( decoder_dim[1], activation='relu')
    
    decoder_mean = Dense(decoder_dim[0], activation='linear')
    
    h_decoded = decoder_h(z)
    
    x_decoded_mean = decoder_mean(h_decoded)

#Wa custom loss function: the sum of a reconstruction term, and the KL divergence regularization term.

    def vae_loss(x, x_decoded_mean):
        xent_loss = encoder_dim[0] * objectives.mean_absolute_error(x, x_decoded_mean)
#        xent_loss = encoder_dim[0] * objectives.binary_crossentropy(x, x_decoded_mean)
        kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
        return xent_loss + kl_loss

    vae = Model(x, x_decoded_mean)
    vae.compile(optimizer='rmsprop', loss=vae_loss, metrics=['mae', 'mse'])
    
    history = vae.fit(train, train,
            shuffle=True,
            nb_epoch=epoch_no,
            batch_size=100,
            verbose = 1,
           validation_data = (train_vali,train_vali))
    
    encoder = Model(x, z_mean)
    
    stop = timeit.default_timer()

    print ("The running takes %r min" %((stop-start)/60))
    
    return encoder, history