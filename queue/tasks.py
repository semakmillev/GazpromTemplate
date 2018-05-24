import os
import uuid
from time import sleep

import imp

import celery
from PIL import ImageCms, ImageChops
from subprocess import call



import sys
#sys.path.insert(0, '../templates')
from celery.result import AsyncResult

sys.path.append('../')
#from .templates import *
from dblite import task
from templates.Layer import Layer
from celery_run import app


@app.task(bind=True)
def add(self, x, y):
    print self.request.id
    sleep(3)
    return x + y

# from engine import generate_picture as gen


def combine_layers(background, foreground_layer):
    left = None
    right = None
    top = None
    bottom = None
    y = None
    if foreground_layer.__class__.__name__ == "ImageLayer":
        if foreground_layer.top is not None:
            y = foreground_layer.top
        if foreground_layer.bottom is not None:
            y = foreground_layer.image_height - (foreground_layer.height + foreground_layer.bottom)
        x = None
        if foreground_layer.left is not None:
            x = foreground_layer.left
        if foreground_layer.right is not None:
            x = foreground_layer.image_width - (foreground_layer.right + foreground_layer.width)
        print "%s, %s" % (x, y)
        print foreground_layer.image
        background.paste(foreground_layer.image, (x, y),
                         mask=foreground_layer.image)
    if foreground_layer.__class__.__name__ == "TextLayer":
        background = foreground_layer.add_to_image(background)
    return background

@app.task(bind=True, name="generate_picture")
def generate_picture(self, template_path, width, height, output="JPEG", resolution=60.0, user_id=None, preview=False):
    extension = output.replace("JPEG", "JPG").lower()
    uid = str(uuid.uuid4())
    if preview:
        file_name = os.path.dirname(os.path.dirname(__file__)) + "/pages/design/preview_" + str(user_id) + "_" + uid + "." + extension
    else:
        file_name = os.path.dirname(os.path.dirname(__file__)) + "/pages/design/result/result_" + str(user_id) + "_" + uid + "." + extension

    f = open(file_name, 'a')

    Layer.image_height = int(height)
    Layer.image_width = int(width)
    a = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/templates/%s/template.py" % template_path
    print a
    foo = imp.load_source("Layer", a)
    layers = foo.layers
    final = layers[0].image
    i = 1
    for layer in layers:
        print i
        i += 1
        final = combine_layers(final, layer)
    f.close()

    from_ = ImageCms.get_display_profile()

    transform = ImageCms.buildTransformFromOpenProfiles("sRGB_Color_Space_Profile.icm", "ISOcoated_v2_300_eci.icc",
                                                        "RGBA", "CMYK")
    final = ImageCms.applyTransform(final, transform)

    if output == "PDF":
        final = ImageChops.invert(final)
        final.save(file_name, output, resolution=resolution)
    elif output == "TIFF":
        final.save(file_name, output, resolution=resolution, compression='tiff_lzw')
    elif output == "JPEG":
        final.save(file_name, output, dpi=(resolution, resolution))
        sleep(0.1)
        s = "exiftool -XResolution=%s -YResolution=%s %s" % (int(resolution), int(resolution), file_name)
        print "!"
        call(s, shell=True)
    # final.save(file_name, output)
    task_id = self.request.id
    print task_id
    task.set_status('%s'%task_id,'SUCCESS',file_name)
    return file_name
