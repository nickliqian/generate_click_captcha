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

# 获取随机的线条颜色
def gen_random_line_color():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = random.randint(0, 255)
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
    word_point_list = []

    word_count = random.randint(3, 5)
    for i in range(0, word_count):
        print("======================")
        while True:
            print(">>>>>>")
            judge = [False] * i
            normal = [True] * i
            location_x = random.randint(width_left_offset, width - width_right_offset)
            location_y = random.randint(height_top_offset, height - height_bottom_offset)
            print(word_point_list)
            print(location_x, location_y)
            for index, wp in enumerate(word_point_list):
                x1, y1 = wp
                if location_x > x1 + word_size + word_offset:
                    judge[index] = True
                elif location_x + word_size + word_offset < x1:
                    judge[index] = True
                elif location_y > y1 + word_size + word_offset:
                    judge[index] = True
                elif location_y + word_size + word_offset < y1:
                    judge[index] = True
                else:
                    print("interference!")
                    continue

            if judge == normal:
                print("break")
                break

        word_point_list.append([location_x, location_y])
        word = random.choice(word_list)
        print(word)
        draw.text((location_x, location_y), word, font=set_font, fill=(0, 0, 0))

    # 干扰线
    if interference_line:
        num = random.randint(inter_line_min, inter_line_max)
        for i in range(num):
            line_x = random.randint(width_left_offset, width - width_right_offset)
            line_y = random.randint(height_top_offset, height - height_bottom_offset)
            line_x_offset = random.randint(-40, 40)
            line_y_offset = random.randint(-40, 40)
            start_point = (line_x, line_y)
            end_point = (line_x + line_x_offset, line_y + line_y_offset)
            draw.line([start_point, end_point], gen_random_line_color(), width=interference_line_width)

    # 干扰虚构文字
    if dummy_word:
        num_a = random.randint(3, 5)  # 虚构文字数量
        for i in range(num_a):
            num_b = random.randint(6, 15)  # 虚构文字笔画数

            # 避免干扰
            while True:
                print(">>>>>>")
                judge = [False] * (i + word_count)
                normal = [True] * (i + word_count)
                location_x = random.randint(width_left_offset, width - width_right_offset)  # x
                location_y = random.randint(height_top_offset, height - height_bottom_offset)  # y
                for index, wp in enumerate(word_point_list):
                    x1, y1 = wp
                    if location_x > x1 + word_size + word_offset:
                        judge[index] = True
                    elif location_x + word_size + word_offset < x1:
                        judge[index] = True
                    elif location_y > y1 + word_size + word_offset:
                        judge[index] = True
                    elif location_y + word_size + word_offset < y1:
                        judge[index] = True
                    else:
                        print("interference!")
                        continue

                if judge == normal:
                    print("break")
                    break
            word_point_list.append([location_x, location_y])
            # 确定位置后开始生成坐标
            bx = random.randint(location_x, location_x + word_size)  # x'
            by = random.randint(location_y, location_y + word_size)  # y'
            line_x_end = location_x + word_size  # x + 20
            line_y_end = location_y + word_size  # y + 20
            a = (bx, location_y)
            b = (line_x_end, by)
            c = (bx, line_y_end)
            d = (location_x, by)
            for j in range(num_b):
                draw_type = random.randint(1, 6)
                if draw_type == 1:
                    draw.line([a, b], (0, 0, 0), width=dummy_word_width)
                elif draw_type == 2:
                    draw.line([a, c], (0, 0, 0), width=dummy_word_width)
                elif draw_type == 3:
                    draw.line([a, d], (0, 0, 0), width=dummy_word_width)
                elif draw_type == 4:
                    draw.line([b, c], (0, 0, 0), width=dummy_word_width)
                elif draw_type == 5:
                    draw.line([b, d], (0, 0, 0), width=dummy_word_width)
                else:  # 6
                    draw.line([c, d], (0, 0, 0), width=dummy_word_width)

    name = name + ".jpg"
    file_path = os.path.join(save_dir, name)
    img.save(file_path)


def main():
    for i in range(5):
        print("pic:{}".format(i))
        gradient = gen_gradient()
        img = gen_gradient_image(gradient)
        put_word_image(img, str(i))


if __name__ == '__main__':
    # 字体大小
    word_size = 32
    # 字符之间的最小距离
    word_offset = 5

    # 图片的宽度和高度
    width = 320
    height = 160

    # 字符距离边界的距离
    width_left_offset = 10
    width_right_offset = 40
    height_top_offset = 10
    height_bottom_offset = 40

    # 图片生成模式
    mode = "RGB"

    # 渐变参数
    no_steps = height

    # 干扰线
    interference_line = False
    inter_line_min = 10
    inter_line_max = 16
    interference_line_width = 3

    # 虚构文字
    dummy_word = True
    dummy_word_width = 2  # 虚构文字的线宽度

    # 其他参数
    word_list = list()
    save_dir = "../image245/"

    with open("../data/chinese_word.json", "r", encoding="utf-8") as f:
        word_list = json.load(f)

    main()
