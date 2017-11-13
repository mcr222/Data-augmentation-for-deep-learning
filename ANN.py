import tensorflow_transfer_inceptionV3 as inception
import tensorflow_3_layer_model as threelayers

'''
Trains an ANN with tensorflow
    transformations -> list of numbers of the transformed sets of images to be used
    dataset -> which dataset to train with
    image_number -> number of images randomly selected from the original dataset to use 
        for training (rest are for testing) need to save which images are use for training 
        to do the test with the other images
    ANN_parameters -> tuple with all parameters for the ANN
'''
def trainANN(model="inception", main_path = "dataset1"):
    #IMPORTANT train path should be unique for all datasets!!!!!
    #IMPORTANTIMPORTANT
    #IMPORTANTIMPORTANT
    train_path = main_path + "/train"
    validation_path = main_path + "/validation"
    if(model=="inception"):
        hist = inception.modelTrain(main_path, train_path, validation_path)
    else:
        hist = threelayer.modelTrain(main_path, train_path, validation_path)
        
    print "Printing training history"
    print hist
    print "List of history for accuracy:"
    print hist.history['val_acc']
    #trainedModel(main_path).summary()
    
trainANN()
    
    

