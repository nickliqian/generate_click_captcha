#!/usr/bin/python
# -*- coding: UTF-8 -*-
from code.click_captcha import ClickCaptcha

if __name__ == '__main__':
    # 创建对象
    c = ClickCaptcha(word_list_file_path="./data/chinese_word.json")

    # 配置开关
    c.enable_add_text = True
    c.enable_interference_line = True
    c.enable_dummy_word = True

    # 创建图形
    c.create_image()

    # 展示和保存
    # c.show()
    c.save("./test.jpg")

    # 批量保存
    c.save_img_dir = "./image245/img"
    c.save_label_dir = "./image245/label"
    c.generate_click_captcha(10)