from PIL import Image, ImageFont, ImageDraw, ImageOps
from random import randint
import string
import random
import os

'''
This transformation adds random text (it can be seen as shapes) on top of
the images.
#TODO: needs parametrization of all hardcoded parameters.
'''
def transformation3(input_folder, output_folder):
    print "applying to " + input_folder + " writing to " + output_folder
    
    for filename in os.listdir(input_folder):
        print(os.path.join(input_folder, filename))
        im=5
        for i in range(im):
            #img.show()
            img = Image.open(input_folder+"/" + filename)
            font = ImageFont.truetype("Verdana.ttf",randint(50,300))
            txt=Image.new('L', (200,200))
            d = ImageDraw.Draw(txt)
            d.text( (0, 0), random.choice(string.letters)+random.choice(string.digits)+random.choice(string.letters)+random.choice(string.digits)+
                    random.choice(string.digits)+random.choice(string.digits)+random.choice(string.letters),  font=font, fill=255)
            w=txt.rotate(randint(0,360),  expand=1)
            img.paste( ImageOps.colorize(w, (0,0,0), (randint(0,255),randint(0,255),randint(0,255))), (randint(-75,75),randint(-75,75)),  w)
    
            img.save(output_folder+"/"+filename.replace(".","_") + str(i) + ".jpg")

#transformation0("backgrounds/fake", "backgrounds/try")
