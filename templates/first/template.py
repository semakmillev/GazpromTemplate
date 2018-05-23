# -*- coding: UTF-8 -*-
# Эти! три строчки всегда в начале шаблона под макет
from math import trunc  # trunc - отбрасывание дробной части. Просто если делишь то используй этот оператор

from templates.Layer import ImageLayer, TextLayer, Layer
import os

diagonal = Layer.get_diagonal()
path = os.path.abspath(os.path.dirname(__file__))+"/files"
ratio = float(ImageLayer.image_width) / float(ImageLayer.image_height)

# Здесь начинается описание шаблона
layer1 = ImageLayer(path + '/G-Energy_2016_billboard_6x3_Desert_carbon.png')
# есть 4 измерения top, bottom, left, right можно заполнить только два из них (т.е. мы отсчитываем только от одного угла)
layer1.top = 0
layer1.left = 0
layer1.width = '100%'
layer1.height = '100%'

layer2 = ImageLayer(path + '/G-Energy_2016_Desert.png')
layer2.top = 0
layer2.right = int(-5000000 / (Layer.image_width ** 2)) if ratio < 1.5 else 0
if ratio > 2:
    layer2.height = '107%'
elif ratio < 1.5:
    layer2.height = '95%'
else:
    layer2.height = '100%'
layer2.width = 'auto'

layer3 = ImageLayer(path + '/G-Energy_2016_billboard_6x3_Desert_logo.png')
layer3.width = trunc(0.25 * diagonal)
# auto значит что сохраняются пропорции, но ведущей является другое измерение
layer3.height = 'auto'
x = trunc(layer3.height * 0.395)
layer3.top = 0
layer3.right = x * 2

layer4 = ImageLayer(path + '/G-Energy-F-Synth-5W-40-4L.png')
layer4.height = trunc(0.207 * diagonal)
layer4.width = 'auto'
layer4.bottom = trunc(x * 0.769)
layer4.left = trunc(x * 1.698)

headtext_layer = TextLayer(font_place=path + "/DINProBold.ttf",
                           font_size=trunc(float(Layer.image_height)*0.09), font_color=(255, 255, 255),
                           text=u"АДАПТАЦИЯ\nК ЛЮБОЙ\nСИТУАЦИИ")
headtext_layer.x = x * 2
headtext_layer.y = layer3.height

wwwtext_layer = TextLayer(font_place=path + "/DINProMedium.ttf",
                          font_size=trunc(float(Layer.image_height)*0.05), font_color=(255, 255, 255),
                          text=u"g-energy.org", align="right")
wwwtext_layer.x = x*2
wwwtext_layer.y = Layer.image_height - x

# здесь просто разом объединить все layer в один массив
layers = [layer1, layer2, layer3, layer4, headtext_layer, wwwtext_layer]
# layers = [layer1, layer2, layer3, layer4]