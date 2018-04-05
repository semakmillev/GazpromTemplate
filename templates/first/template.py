# -*- coding: UTF-8 -*-
# Эти три строчки всегда в начале шаблона под макет
from math import trunc  # trunc - отбрасывание дробной части. Просто если делишь то используй этот оператор

from templates.Layer import ImageLayer, TextLayer, Layer

diagonal = Layer.get_diagonal()
# Здесь начинается описание шаблона
layer1 = ImageLayer('templates/first/G-Energy_2016_billboard_6x3_Desert_carbon.png')
# есть 4 измерения top, bottom, left, right можно заполнить только два из них (т.е. мы отсчитываем только от одного угла)
layer1.top = 0
layer1.left = 0
layer1.width = '100%'
layer1.height = '100%'

layer2 = ImageLayer('templates/first/G-Energy_2016_Desert.png')
layer2.top = 0
layer2.right = 0
layer2.width = '75%'
# % - проценты от размера итогового изображения
layer2.height = '100%'

layer3 = ImageLayer('templates/first/G-Energy_2016_billboard_6x3_Desert_logo.png')
layer3.width = trunc(0.25 * diagonal)
# auto значит что сохраняются пропорции, но ведущей является другое измерение
layer3.height = 'auto'
x = trunc(layer3.height * 0.395)
layer3.top = 0
layer3.right = x * 2

layer4 = ImageLayer('templates/first/G-Energy-F-Synth-5W-40-4L.png')
layer4.height = trunc(0.2 * diagonal)
layer4.width = 'auto'
layer4.bottom = x
layer4.left = x * 2
text_layer = TextLayer(font_place="templates/first/DINProMedium.ttf",
                       font_size=trunc(30 * (float(Layer.image_width) / 1000)), font_color=(255, 255, 255),
                       text=u"АДАПТАЦИЯ\nК ЛЮБОЙ СИТУАЦИИ")
text_layer.x = x * 2
text_layer.y = layer3.height

# здесь просто разом объединить все layer в один массив
layers = [layer1, layer2, layer3, layer4, text_layer]
# layers = [layer1, layer2, layer3, layer4]
