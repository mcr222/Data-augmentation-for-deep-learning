from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import tensorflow_interface
import os
import ANN_constants as ANN


'''
rescale is a value by which we will multiply the data before any other processing. 
Our original images consist in RGB coefficients in the 0-255, but such values would 
be too high for our models to process (given a typical learning rate), so we target 
values between 0 and 1 instead by scaling with a 1/255. factor.
'''
#WARNING!! rescaling should be the same for train and test
#train_datagen = ImageDataGenerator()
datagen = ImageDataGenerator(rescale=1. / 255)

def countSamples(path):
    file_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
    return file_count 

# this is a generator that will read pictures found in
# subfolders of 'data/train', and indefinitely generate
# batches of augmented image data
def getGenerator(data_dir = 'dataset1/train'):
    generator = datagen.flow_from_directory(
        data_dir,
        target_size=(ANN.img_width, ANN.img_height),
        batch_size=ANN.batch_size,
        class_mode='binary')
    return generator

def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    return model


def getWeightsPath(path):
    return path + '/3layer_weights.h5'

def modelTrain(path, train_path, validation_path):
    #IMPORTANT: model only will train with batches,
    #thus training images not fitting exactly into
    #a batch size won't be used
    model = create_model(ANN.input_shape)
    train_generator = getGenerator(train_path)
    validation_generator = getGenerator(validation_path)
    nb_train_samples =  countSamples(train_path)
    nb_validation_samples = countSamples(validation_path)
    
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // ANN.batch_size,
        epochs=ANN.epochs,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // ANN.batch_size)

    model.save_weights(getWeightsPath(path))
    return history


def trainedModel(path):   
    # build the VGG16 network
    model = create_model(ANN.input_shape)
    model.load_weights(getWeightsPath(path))
    return model



