import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import os
import ANN_constants as ANN

datagen = ImageDataGenerator(rescale=1. / 255)

def countSamples(path):
    file_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
    return file_count 

# this is a generator that will read pictures found in
# subfolders of 'data/train', and indefinitely generate
# batches of augmented image data
def getGenerator(data_dir):
    #cannot shuffle to have the same order when training
    #top layer
    generator = datagen.flow_from_directory(
        data_dir,
        target_size=(ANN.img_width, ANN.img_height),
        batch_size=ANN.batch_size,
        class_mode=None,
        shuffle=False)
    return generator

def get_base_model():
    model = applications.InceptionV3(weights='imagenet', include_top=False, input_shape=ANN.input_shape)
    model.trainable = False
    return model

def bottleneck_path(path,image_path):
    return path + '/bottleneck_features_'+image_path.replace("/","_").replace(".","_")+'.npy'
    
#must do this with train and validation path
def save_bottlebeck_features(path, image_path, nb_samples):
    if(os.path.isfile(bottleneck_path(path,image_path))):
        print "Features already computed for InceptionV3"
        return
    print "Saving features after InceptionV3 for: " + image_path
    # build the InceptionV3 network
    model = get_base_model()

    bottleneck_features_train = model.predict_generator(
        getGenerator(image_path), nb_samples // ANN.batch_size)
    np.save(open(bottleneck_path(path,image_path), 'w'),
            bottleneck_features_train)
    
    print "Features saved"

def get_top_model(shape):
    top_model = Sequential()
    top_model.add(Flatten(input_shape=shape))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(1, activation='sigmoid'))
    
#     x = Flatten()(base_model.output)
#     x = Dense(4096, activation='relu')(x)
#     x = Dropout(0.5)(x)
#     x = BatchNormalization()(x)
#     predictions = Dense(num_classes, activation = 'softmax')(x)
    return top_model

def getWeightsPath(path):
    return path + '/transferinception_weights.h5'


'''
 validation_data: Data on which to evaluate
                the loss and any model metrics
                at the end of each epoch. The model will not
                be trained on this data.
'''
def modelTrain(path, train_path, validation_path):
    nb_train_samples = countSamples(train_path)
    nb_validation_samples = countSamples(validation_path)
    
    save_bottlebeck_features(path, train_path, nb_train_samples)
    save_bottlebeck_features(path, validation_path, nb_validation_samples)
    
    train_data = np.load(open(bottleneck_path(path, train_path)))
    train_labels = np.array(
        [0] * (nb_train_samples / 2) + [1] * (nb_train_samples / 2))

    validation_data = np.load(open(bottleneck_path(path, validation_path)))
    validation_labels = np.array(
        [0] * (nb_validation_samples / 2) + [1] * (nb_validation_samples / 2))

    model = get_top_model(train_data.shape[1:])
    
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    #training sample number and validation sample number must be 
    #whole times of the batch_size 16.
    history = model.fit(train_data, train_labels,
              epochs=ANN.epochs,
              batch_size=ANN.batch_size,
              validation_data=(validation_data, validation_labels))
    
    model.save_weights(getWeightsPath(path))
    return history

def trainedModel(path):   
    # build the InceptionV3 network
    # weights will be downoaded the first time this executes
    base_model = get_base_model()
    #base_model.summary()
    # build a classifier model to put on top of the convolutional model
    top_model = get_top_model(base_model.output_shape[1:])
    top_model.load_weights(getWeightsPath(path))
    #top_model.summary()
     #create graph of your new model
    head_model = Model(input= base_model.input, output= top_model(base_model.output))
    
    # add the model on top of the convolutional base
#     model.add(top_model)
    return head_model


