from keras import backend as K

# dimensions of our images.
img_width, img_height = 150, 150
epochs = 2
batch_size = 16
input_shape = (img_width, img_height, 3)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
    
