# -*- coding: UTF-8 -*-

from PIL import Image
import math

from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype


class Layer(object):
    image_height = 100
    image_width = 300

    def __init__(self):
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None
        # self.__image_place = ''

    @staticmethod
    def get_diagonal():
        return math.trunc(math.sqrt(Layer.image_height ** 2 + Layer.image_width ** 2))


class TextLayer(Layer):
    def __init__(self, font_place, font_size, font_color, text):
        super(TextLayer, self).__init__()
        self.font = truetype(font=font_place, size=font_size)
        self.font_color = font_color
        self.text = text
        self.__x = 0
        self.__y = 0

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y):
        ascent, descent = self.font.getmetrics()
        self.__y = y - ascent

    def add_to_image(self, image):
        draw = Draw(image)
        draw.text((self.x, self.y), self.text, self.font_color, font=self.font)
        return image

    x = property(get_x, set_x)
    y = property(get_y, set_y)


class ImageLayer(Layer):
    def __init__(self, image_place):
        super(ImageLayer, self).__init__()
        self.__image = Image.open(image_place)
        width, height = self.__image.size
        self.__width = str(width)
        self.__height = str(height)

    def set_height(self, height):
        self.__height = str(height)

    def get_height(self):

        if int(str(self.__height.find("%"))) > -1:
            return int(self.__height.replace("%", "")) * self.image_height / 100
        elif int(str(self.__height.find('auto'))) > -1:
            width, height = self.__image.size
            return math.trunc(height * self.width / width)
        else:
            return int(self.__height)

    def set_width(self, width):
        self.__width = width

    def get_width(self):
        if int(str(self.__width).find("%")) > -1:
            return int(self.__width.replace("%", "")) * self.image_width / 100
        elif int(str(self.__width).find('auto')) > -1:
            width, height = self.__image.size
            return math.trunc(width * self.height / height)
        else:
            return int(self.__width)

    def set_image(self, image_place):
        self.__image = Image.open(image_place)
        width, height = self.__image.size
        self.__width = str(width)
        self.__height = str(height)

    def get_image(self):
        img = self.__image.resize((self.width, self.height))
        return img

    def check_places(self):
        if (self.top is None and self.bottom is None) or (self.top is not None and self.bottom is not None):
            raise Exception('Check Place', 'Error in top/bottom pair')
        if (self.right is None and self.left is None) or (self.right is not None and self.left is not None):
            raise Exception('Check Place', 'Error in left/right pair')

    height = property(get_height, set_height)
    width = property(get_width, set_width)
    image = property(get_image, set_image)
