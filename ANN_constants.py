from keras import backend as K

# dimensions of our images.
img_width, img_height = 150, 150
epochs = 20
#https://stats.stackexchange.com/questions/164876/tradeoff-batch-size-vs-number-of-iterations-to-train-a-neural-network
batch_size = 1
input_shape = (img_width, img_height, 3)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
    
