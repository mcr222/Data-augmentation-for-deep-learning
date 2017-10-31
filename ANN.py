import Data_augmentation as da
import tensorflow as tf


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

