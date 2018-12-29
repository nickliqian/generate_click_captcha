#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont
import math, string
import codecs


class RandomChar():
    @staticmethod
    def Unicode():
        val = random.randint(0x4E00, 0x9FBF)
        return chr(val)

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        str = "%x" % val
        #   return str.decode('hex').decode('gb2312')
        # return str.encode('gb2312').decode('gb2312')
        return codecs.decode(str, 'hex_codec').decode('gb2312')


class ImageChar():
    def __init__(self, fontColor=(0, 0, 0),
                 size=(100, 40),
                 # fontPath='C:/Windows/Fonts/wqy.ttc',
                 fontPath='C:/Windows/Fonts/simsun.ttc',
                 bgColor=(255, 255, 255),
                 fontSize=20):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor)

    def rotate(self):
        self.image.rotate(random.randint(0, 30), expand=0)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        #  print(pos)
        # print(txt)
        # print(self.font)
        # print(fill)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

    def randRGB(self):
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))

    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, 1):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw

    def randChinese(self, num):
        gap = 5
        start = 0
        for i in range(0, num):
            char = RandomChar().GB2312()
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-5, 5)), RandomChar().GB2312(), self.randRGB())
            self.rotate()
        self.randLine(18)

    def save(self, path):
        self.image.save(path)


if __name__ == '__main__':
    ic = ImageChar(fontColor=(100, 211, 90))
    ic.randChinese(4)
    ic.save("5.jpeg")