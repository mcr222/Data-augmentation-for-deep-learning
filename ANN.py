import tensorflow_transfer_inceptionV3 as inception
import tensorflow_3_layer_model as threelayers
import os
import sys

'''
Trains an ANN with tensorflow
    
'''
from matplotlib.font_manager import path
def trainANN(model="inception", main_path = "dataset1"):
    print "Training model " + model + " on dataset: " + main_path
    result_path = main_path+"/result_"+model+".txt"
    if(os.path.isfile(result_path)):
        print "Model already trained in this dataset"
        return
    
    train_path = main_path + "/training"
    validation_path = main_path + "/test"
    if(model=="inception"):
        hist = inception.modelTrain(main_path, train_path, validation_path)
        #inception.trainedModel(main_path).summary()
    else:
        hist = threelayers.modelTrain(main_path, train_path, validation_path)
        #threelayers.trainedModel(main_path).summary()
        
    print "Printing training history"
    print hist
    print "List of history for validation accuracy in path " + main_path + " on model " + model
    print hist.history['val_acc']
    
    newstr = ''.join([''+ str(i)+', ' for i in hist.history['val_acc']])
    print newstr
    with open(result_path,"w") as f:
        f.write(newstr)

#TODO: find . -name "*init*" -delete to remove init files created by system when generating images
root_path = "ex_dataset/"
for dataset_path in os.listdir(root_path):
    try:
        trainANN("inception",root_path+dataset_path)
    except Exception as e:
        print "ERROR!!!! Inception complains (probably batch size)"
        print e
        
    try:
        trainANN("threelayers",root_path+dataset_path)
    except Exception as e:
        print "ERROR!!!! Three layers complains (probably batch size)"
        print e
    

