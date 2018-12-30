#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
根据此文编写：https://www.cnblogs.com/whu-zeng/p/4855480.html
"""
import random
from PIL import Image, ImageDraw, ImageFont
import codecs


class RandomChar(object):
    @staticmethod
    def tran_unicode():
        val = random.randint(0x4E00, 0x9FBF)
        return chr(val)

    @staticmethod
    def tran_gb2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        string_value = "%x" % val
        return codecs.decode(string_value, 'hex_codec').decode('gb2312')


class ImageChar(object):
    def __init__(self, font_color=(0, 0, 0), size=(100, 40), font_path='C:/Windows/Fonts/simkai.ttf',
                 bg_color=(255, 255, 255), font_size=20):
        self.size = size
        self.fontPath = font_path
        self.bgColor = bg_color
        self.fontSize = font_size
        self.fontColor = font_color
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bg_color)

    def rotate(self):
        self.image.rotate(random.randint(0, 90), expand=0)

    def draw_text(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.multiline_text(xy=pos, text=txt, font=self.font, fill=fill)
        del draw

    @staticmethod
    def rand_rgb():
        return (random.randint(2, 220),
                random.randint(2, 220),
                random.randint(2, 220))

    def rand_point(self):
        width, height = self.size
        return random.randint(0, width), random.randint(0, height)

    def rand_line(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.rand_point(), self.rand_point()], self.rand_rgb())
        del draw

    def rand_chinese(self, num):
        gap = 5
        start = 0
        for i in range(0, num):
            char = RandomChar().tran_gb2312()
            print(char)
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.draw_text((x, random.randint(0, 15)), char, self.rand_rgb())
            self.rotate()
        self.rand_line(5)

    def save(self, path="test.jpg"):
        self.image.save(path)

    def show(self):
        self.image.show()


def main():
    ic = ImageChar(font_color=(100, 211, 90))
    ic.rand_chinese(4)
    ic.show()


if __name__ == '__main__':
    main()
