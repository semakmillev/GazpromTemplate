# -*- coding: UTF-8 -*-
# Эти пять строчек всегда в начале шаблона под макет
from math import trunc  # trunc - отбрасывание дробной части. Просто если делишь то используй этот оператор

from templates.Layer import ImageLayer, TextLayer, Layer
import os

diagonal = Layer.get_diagonal()
path = os.path.abspath(os.path.dirname(__file__))
ratio = float(ImageLayer.image_width) / float(ImageLayer.image_height)

# Здесь начинается описание шаблона