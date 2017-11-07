import Augmentor
import os
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageEnhance
from random import randint
from os.path import basename

dataset_folder = "data/dataset"
original_images = "/original"
transformation_images = "/transformation"
test_folder = "data/testFolder/original"
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


# -------------------------------------------------------------------------------------------------------------- #
# -------------------------------------- Transformations --------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------#


'''
Basic Transformations. 
Generate an output dataset using the following basic transformations:
rotation, zoom, crops?, horizontal flip, shearing
'''
def transformation0(input_folder, output_folder):
    print ("Applying to " + input_folder + " writing to " + output_folder)
    p = Augmentor.Pipeline(input_folder)
    p.rotate(probability=0.5, max_left_rotation=20, max_right_rotation=20)
    p.zoom(probability=0.5, min_factor=1.1, max_factor=1.5)
    p.flip_left_right(probability=0.5)
    p.shear(probability=0.5, max_shear_left=20, max_shear_right=20)

    #Calculate number of samples (initially same size of the dataset)
    total_samples = len(os.listdir(input_folder)) - 2
    print("generating " + str(total_samples) + " samples")
    p.sample(total_samples)


'''
Image deformation LIGHT
Generate an output dataset using the random transformation and gaussian distortion from  Augmentor
The magnitude parameter is set to 3 
'''
def transformation1(input_folder, output_folder):
    print ("Applying to " + input_folder + " writing to " + output_folder)
    p = Augmentor.Pipeline(input_folder)
    val = random.randint(1, 9999)
    if val%2 ==0:
        p.random_distortion(probability=1, grid_width=10, grid_height=10, magnitude=3)
    else:
        p.gaussian_distortion(probability=1, grid_height=10, grid_width=10, magnitude=3, corner="bell", method= "out")

    # Calculate number of samples (initially same size of the dataset)
    total_samples = len(os.listdir(input_folder)) - 2
    print("generating " + str(total_samples) + " samples")
    p.sample(total_samples)

'''
Image deformation HEAVY
Generate an output dataset using the random transformation and gaussian distortion from  Augmentor
The magnitude parameter is set to 8
'''
def transformation2(input_folder, output_folder):
    print ("Applying to " + input_folder + " writing to " + output_folder)
    p = Augmentor.Pipeline(input_folder)
    val = random.randint(1, 9999)
    if val%2 ==0:
        p.random_distortion(probability=1, grid_width=10, grid_height=10, magnitude=8)
    else:
        p.gaussian_distortion(probability=1, grid_height=10, grid_width=10, magnitude=8, corner="bell", method= "out")

    # Calculate number of samples (initially same size of the dataset)
    total_samples = len(os.listdir(input_folder)) - 2
    print("generating " + str(total_samples) + " samples")
    p.sample(total_samples)


'''
Color Deformation
Generate an output dataset using transformations: 
saturation, contrast, brightness
'''
def transformation3(input_folder, output_folder):
    print ("Applying to " + input_folder + " writing to " + output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPEG"):
         img = Image.open(input_folder + str("/") + file)
         newImg = img
         r1=randint(1,10)
         r2=randint(1,10)
         r3=randint(1,10)

         if r1%2==0:
            contrast = ImageEnhance.Contrast(img)
            newImg = contrast.enhance(randint(1,5))

         if r2 % 2 == 0:
             brightness = ImageEnhance.Brightness(newImg)
             newImg = brightness.enhance(randint(1,5))

         if r3 % 2 == 0:
             color = ImageEnhance.Color(newImg)
             newImg = color.enhance(0.2)

         newImg.save(output_folder +  "/" + basename(file) + str("_mod.jpg"))

'''
This transformation adds random text (it can be seen as shapes) on top of
the images.
#TODO: needs parametrization of all hardcoded parameters.
'''
def transformation4(input_folder, output_folder):
    print ("applying to " + input_folder + " writing to " + output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        print(os.path.join(input_folder, filename))
        im = 1

        if(filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg")):
            for i in range(im):
                # img.show()
                img = Image.open(input_folder + "/" + filename)
                font = ImageFont.truetype("Verdana.ttf", random.randint(50, 300))
                txt = Image.new('L', (200, 200))
                d = ImageDraw.Draw(txt)
                d.text((0, 0), random.choice(string.ascii_letters) + random.choice(string.digits) + random.choice(
                    string.ascii_letters) + random.choice(string.digits) +
                       random.choice(string.digits) + random.choice(string.digits) + random.choice(string.ascii_letters),
                       font=font, fill=255)
                w = txt.rotate(randint(0, 360), expand=1)
                img.paste(ImageOps.colorize(w, (0, 0, 0), (randint(0, 255), randint(0, 255), randint(0, 255))),
                          (randint(-75, 75), randint(-75, 75)), w)

                img.save(output_folder + "/" + filename.replace(".", "_") + str(i) + ".jpg")



# -------------------------------------------------------------------------------------------------------------- #
# -------------------------------------- Auxiliary functions ----------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------#

'''
Resize images from a specified folder to 150X150
@input_folder - specified folder
'''
def resizeImages(input_folder):
    p = Augmentor.Pipeline(input_folder)
    p.resize(probability=1, width=150, height=150)

    # Calculate number of samples (initially same size of the dataset)
    total_samples = len(os.listdir(input_folder)) - 2
    print("generating " + str(total_samples) + " samples")
    p.sample(total_samples)

'''
Rename files from a specified folder with a random name
@input_folder - specified folder
'''
def renameFiles(input_folder):
    for file in os.listdir(input_folder):
        rand = random.randint(1, 999999)
        os.rename(input_folder + "/" + file, input_folder + "/" + str(rand) + "_2.jpg")


#list_transformations = [transformation0, transformation1]
#dataAugmentation(0,0)
#transformation1(test_folder, output_folder="data/testFolder/output")
#transformation2(input_folder="data/dataset4/original", output_folder=getImageFolder(0,0))
#transformation4(input_folder="data/dataset4/original", output_folder="data/dataset4/dataset4_transformation4")
#transformation3(input_folder="data/dataset4/original", output_folder="data/dataset4/dataset4_transformation3")