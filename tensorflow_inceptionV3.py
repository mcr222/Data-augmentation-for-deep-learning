from keras.applications import InceptionV3
'''
We use InceptionV3 to see how it behaves without the 
default weights for the classes there exist in Imagenet. 
It makes not sense to train it with our datasets
'''

#PROBLEM: InceptionV3 with top requires 299x299 images
def create_model(input_shape=(150,150,3)):
    cnn = InceptionV3(include_top=True, classes=1, weights=None)
    cnn.trainable = False

