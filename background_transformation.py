from PIL import Image, ImageFont, ImageDraw, ImageOps
from random import randint
import os
from posix import mkdir

dataset = "4"
png_source = "pngs/dataset"+dataset+"/"
#we will force object to be 120x120
size=(120,120)
#background images are already of size 150x150
which_background = "fake"
which_background = "real"

background_path = "background/" + which_background + "/"

output_folder = "pngs/dataset"+dataset+"_" + which_background +"/"
try:
    mkdir(output_folder)
except:
    pass
    
 
for background_filename in os.listdir(background_path):
    for foreground_filename in os.listdir(png_source):
        print background_filename + "  " + foreground_filename
        background = Image.open(background_path+background_filename)
        foreground = Image.open(png_source+foreground_filename)
        foreground.thumbnail(size, Image.ANTIALIAS)
        foreground.convert('RGBA')
        #foreground.save("moto.png","png")
        background.paste(foreground, (randint(0,50), randint(0,50)), foreground)
        background.save(output_folder + background_filename.replace(".","_") + foreground_filename.replace(".","_") + ".jpg")

