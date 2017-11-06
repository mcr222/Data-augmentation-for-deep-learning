import tensorflow as tf
from keras.applications import InceptionV3
from keras import layers
from keras.models import Model
import keras
from keras.preprocessing.image import ImageDataGenerator

print "Start training"

batch_size = 16
train_datagen = ImageDataGenerator()

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'try',  # this is the target directory
        target_size=(299, 299),  # all images will be resized to 299x299
        batch_size=batch_size,
        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels


cnn = InceptionV3(include_top=True, classes=1, weights=None)
cnn.trainable = True

cnn.compile(optimizer="sgd", loss="mean_squared_error")
#cnn.summary()

cnn.fit_generator(
        train_generator,
        steps_per_epoch=2000 // batch_size,
        epochs=50)
cnn.save_weights('first_try.h5')  # always save your weights after training or during training

