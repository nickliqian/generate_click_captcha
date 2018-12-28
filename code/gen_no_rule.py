#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image
import random

img = Image.new("RGB", (640, 480), (0, 255, 0))

w, h = img.size

for i in range(h):
    for j in range(w):
        a = random.randint(50, 100)
        b = random.randint(100, 150)
        c = random.randint(150, 200)
        img.putpixel((j, i), (a, b, c))
img.show()