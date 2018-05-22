# -*- coding: UTF-8 -*-
import imp
import os
import uuid
from subprocess import call
from time import sleep
from PIL import ImageCms, ImageChops


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


def generate_picture(template_path, width, height, output="JPEG", resolution=60.0, user_id=None, preview=False, ):
    extension = output.replace("JPEG", "JPG").lower()
    uid = str(uuid.uuid4())
    if preview:
        file_name = os.path.dirname(__file__) + "/pages/design/preview_" + str(user_id) + "_" + uid + "." + extension
    else:
        file_name = os.path.dirname(__file__) + "/result_" + str(user_id) + "_" + uid + "." + extension

    f = open(file_name, 'a')
    from templates.Layer import Layer
    Layer.image_height = int(height)
    Layer.image_width = int(width)
    a = os.path.abspath(os.path.dirname(__file__)) + "/templates/%s/template.py" % template_path
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
    # final = final.convert('RGB')
    # final = final.convert('CMYK')

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
    print "!!!"
    return file_name


# layer1 = layers[0]




'''
im = Image.open("template/G-Energy-F-Synth-5W-40-4L.png")
font = truetype(font="template/DINProRegular.ttf", size=108)
ascent, descent = font.getmetrics()
(width, baseline), (offset_x, offset_y) = font.font.getsize("test")
print ascent - offset_y

draw = Draw(im)
draw.text((0, 0), "Sample Text", (255, 255, 0), font=font)
im.save("out.png")
'''
# im = im.resize((100, 200))
# l = layers[0]
# print l
'''

'''
