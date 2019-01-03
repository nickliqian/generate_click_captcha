#!/usr/bin/python
# -*- coding: UTF-8 -*-
from code.click_captcha import ClickCaptcha

if __name__ == '__main__':
    # 创建对象
    c = ClickCaptcha()
    c.font_settings(font_path="C:/windows/fonts/simkai.ttf", word_list_file_path="data/chinese_word.json")
    # 配置开关
    c.enable_add_text = True  # 添加文字

    # 模板路径
    c.template_path = "code/exp.xml"

    # 保存路径
    c.save_img_dir = "image245/img"
    c.save_label_dir = "image245/label"

    a = 3

    # 创建图形和保存
    if a == 1:
        c.create_image()
        c.save("test.jpg")
        c.show()
    # 批量保存
    if a == 2:
        c.enable_interference_line = True  # 添加干扰线
        c.enable_dummy_word = True  # 添加虚构文字对象
        c.create_image_by_batch(1)
    if a == 3:
        c.enable_interference_line = False  # 添加干扰线
        c.enable_dummy_word = True  # 添加虚构文字对象
        c.create_image_by_batch(20)


