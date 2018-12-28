#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw, ImageFont
import random
import json
import os


# 获取随机的一种背景色
def gen_random_color():
    a = random.randint(0, 255)
    b = random.randint(50, 255)
    c = random.randint(50, 255)
    return a, b, c


# 计算每层的渐变色数值
def lerp_colour(c1, c2, t):
    return int(c1[0] + (c2[0] - c1[0]) * t),\
           int(c1[1] + (c2[1] - c1[1]) * t),\
           int(c1[2] + (c2[2] - c1[2]) * t)


# 生成渐变色列表
def gen_gradient():
    list_of_colors = [gen_random_color(), gen_random_color(), gen_random_color(), gen_random_color()]
    gradient = []
    # for i in range(len(list_of_colors) - 2):
    #     for j in range(no_steps):
    #         colour = lerp_colour(list_of_colors[i], list_of_colors[i + 1], j / no_steps)

    for i in range(len(list_of_colors) - 2):
        for j in range(no_steps):
            gradient.append(lerp_colour(list_of_colors[i], list_of_colors[i + 1], j / no_steps))
    return gradient


# 生成一张渐变色背景的图片
def gen_gradient_image(gradient):
    img = Image.new(mode, (width, height), (0, 0, 0))

    for i in range(height):
        for j in range(width):
            img.putpixel((j, i), gradient[j])
    return img


def put_word_image(img, name):
    set_font = ImageFont.truetype('C:/windows/fonts/simkai.ttf', word_size)
    draw = ImageDraw.Draw(img)

    word_count = random.randint(3, 5)
    word_point_list = []
    for i in range(0, word_count):
        print("======================")
        judge = [False] * i
        normal = [True] * i
        while True:
            print(">>>>>>")
            location_x = random.randint(width_offset, width - width_offset)
            location_y = random.randint(height_offset, height - height_offset)
            print(word_point_list)
            print(location_x, location_y)
            for index, wp in enumerate(word_point_list):
                wp_x, wp_y = wp
                if wp_x < location_x < wp_x + word_size:
                    print("wp_x < location_x < wp_x + word_size")
                    pass
                elif wp_y < location_y < wp_y + word_size:
                    print("wp_y < location_y < wp_y + word_size")
                    pass
                elif wp_x < location_x + word_size < wp_x + word_size:
                    print("wp_x < location_x + word_size < wp_x + word_size")
                    pass
                elif wp_y < location_y + word_size < wp_y + word_size:
                    print("wp_y < location_y + word_size < wp_y + word_size")
                    pass
                else:
                    judge[index] = True

            if judge == normal:
                print("break")
                break

        word_point_list.append([location_x, location_y])
        word = random.choice(word_list)
        print(word)
        draw.text((location_x, location_y), word, font=set_font, fill=(0, 0, 0))
    name = name + ".jpg"
    file_path = os.path.join(save_dir, name)
    img.save(file_path)


def main():
    for i in range(500):
        print("pic:{}".format(i))
        gradient = gen_gradient()
        img = gen_gradient_image(gradient)
        put_word_image(img, str(i))


if __name__ == '__main__':
    word_size = 20
    width = 320
    height = 160
    width_offset = 30
    height_offset = 20
    mode = "RGB"
    no_steps = height
    word_list = list()
    save_dir = "../image245/"

    with open("../data/chinese_word.json", "r", encoding="utf-8") as f:
        word_list = json.load(f)

    main()
