#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw, ImageFont
import random
import json
import os


# 获取随机的一种背景色（去掉了偏黑系颜色）
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


# 生成一个随机的位置，且判断不与之前的位置重合
def generate_random_location(i_num, word_point_list):
    print("======================")
    while True:
        print(">>>>>>")
        judge = [False] * i_num
        normal = [True] * i_num
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
            return location_x, location_y


def add_interference_line(draw):
    num = random.randint(inter_line_min, inter_line_max)
    for i in range(num):
        line_x = random.randint(width_left_offset, width - width_right_offset)
        line_y = random.randint(height_top_offset, height - height_bottom_offset)
        line_x_offset = random.randint(*interference_line_radius)
        line_y_offset = random.randint(*interference_line_radius)
        start_point = (line_x, line_y)
        end_point = (line_x + line_x_offset, line_y + line_y_offset)
        draw.line([start_point, end_point], gen_random_line_color(), width=interference_line_width)


def add_dummy_word(draw, word_count, word_point_list):
    # 虚构文字数量
    num_a = random.randint(dummy_word_count_min, dummy_word_count_max)
    for i in range(num_a):
        # 虚构文字笔画数
        num_b = random.randint(dummy_word_strokes_min, dummy_word_strokes_max)

        # 生成随机位置+避免互相干扰
        location_x, location_y = generate_random_location(i + word_count, word_point_list)

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


def put_word_image(img, name):
    # 设置字体
    set_font = ImageFont.truetype(font_path, word_size)
    # 初始化绘画对象和所有对象的位置
    draw = ImageDraw.Draw(img)
    word_point_list = []

    word_count = random.randint(3, 5)
    for i in range(0, word_count):
        # 生成随机位置 + 避免互相干扰
        location_x, location_y = generate_random_location(i, word_point_list)

        # 对象位置加入到列表
        word_point_list.append([location_x, location_y])

        # 随机选择文字并绘制
        word = random.choice(word_list)
        print(word)
        draw.text((location_x, location_y), word, font=set_font, fill=(0, 0, 0))

    # 创建干扰线
    if interference_line:
        add_interference_line(draw)

    # 创建干扰虚构文字
    if dummy_word:
        add_dummy_word(draw, word_count, word_point_list)

    if save_status:
        name = "{}.{}".format(name, image_postfix)
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

    # 字体和字符集
    font_path = "C:/windows/fonts/simkai.ttf"
    word_list = list()
    # 字符集从文件中读取的时候必须是数组形式
    with open("../data/chinese_word.json", "r", encoding="utf-8") as f:
        word_list = json.load(f)

    # 干扰线
    interference_line = False
    inter_line_min = 10
    inter_line_max = 16
    interference_line_width = 3
    interference_line_radius = (-40, 40)

    # 虚构文字
    dummy_word = True
    dummy_word_width = 2  # 虚构文字的线宽度
    dummy_word_count_min = 3
    dummy_word_count_max = 5
    dummy_word_strokes_min = 6
    dummy_word_strokes_max = 15

    # 图片保存路径
    save_status = True
    image_postfix = "jpg"
    save_dir = "../image245/"

    main()
