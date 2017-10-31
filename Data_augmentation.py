

dataset_folder = "data/dataset"
original_images = "/original"
transformation_images = "/transformation"

'''
Applies a data augmentation technique into a dataset
    transformation -> which # of transformation to apply, if -1 return original folder
    dataset -> which # of dataset to apply to
'''
def getImageFolder(transformation, dataset):
    if(transformation <0):
        return dataset_folder+str(dataset)+original_images
    
    return dataset_folder+str(dataset)+transformation_images+str(transformation)



'''
Applies a data augmentation technique into a dataset
    transformation -> which # of transformation to apply
    dataset -> which # of dataset to apply to
'''
def dataAugmentation(transformation, dataset):
  list_transformations[transformation](getImageFolder(-1,dataset),getImageFolder(transformation,dataset)) 
    
'''
Explain transformation
'''
def transformation0(input_folder, output_folder):
    print "applying to " + input_folder + " writing to " + output_folder

'''
Explain transformation
'''
def transformation1(input_folder, output_folder):
    print "applying to " + input_folder + " writing to " + output_folder
    
list_transformations = [transformation0, transformation1]

dataAugmentation(0,0)

