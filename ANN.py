from keras import backend as K


# dimensions of our images.
img_width, img_height = 150, 150
epochs = 2
batch_size = 16
input_shape = (img_width, img_height, 3)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)

'''
Trains an ANN with tensorflow
    transformations -> list of numbers of the transformed sets of images to be used
    dataset -> which dataset to train with
    image_number -> number of images randomly selected from the original dataset to use 
        for training (rest are for testing) need to save which images are use for training 
        to do the test with the other images
    ANN_parameters -> tuple with all parameters for the ANN
'''
def trainANN(transformations, dataset, image_number, ANN_parameters):
    print "training"

