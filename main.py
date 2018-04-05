# -*- coding: UTF-8 -*-
import imp



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


def generate_picture(template_name, width, height):
    from templates.Layer import Layer
    Layer.image_height = int(height)
    Layer.image_width = int(width)
    foo = imp.load_source("Layer", "./templates/%s/template.py" % template_name)
    layers = foo.layers
    final = layers[0].image
    i = 1
    for layer in layers:
        print i
        i += 1
        final = combine_layers(final, layer)
    final.save("res.png")

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
