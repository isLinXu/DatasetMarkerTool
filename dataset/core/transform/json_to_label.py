
import os
import cv2
import numpy as np
import json

from matplotlib import pyplot as plt


def json_to_label(json_path, label_save_path,  path_allclass_txt, label_size=(224, 224)):
    """
    该函数直接由.json文件生成单通道8位标签图像,各类位置区域像素对应各类序号0,1,2,3,4......等
    :param json_path: 包含.json文件的文件夹路径
    :param label_save_path: 标签存放位置
    :param path_allclass_txt: 包含所有类别的txt文件路径
    :param label_size: 标签图像的大小
    :return:
    """
    class_txt = open(path_allclass_txt, "r")
    category_types = class_txt.read().splitlines()
    print('All class name:\n', category_types)

    for file in os.listdir(json_path):
        mask = np.zeros([label_size[1], label_size[0], 1], np.uint8)  # 创建一个大小和原图相同的空白图像
        with open(os.path.join(json_path, file), "r") as f:
            label = json.load(f)
        shapes = label["shapes"]
        for shape in shapes:
            category = shape["label"]
            points = shape["points"]
            points_array = np.array(points, dtype=np.int32)# 填充
            mask = cv2.fillPoly(mask, [points_array], category_types.index(category)) #在对应位置填充类别序号
        name = file.split('.')[0]
        cv2.imwrite(label_save_path + '/' + name + ".png", mask)
    print('json file process ok, get %d label images' % len(os.listdir(json_path)))


def bit24_to_bit8(bit24_path, bit8_path):
    for file in os.listdir(bit24_path):
        img1 = cv2.imread(bit24_path + '/' + file, -1)
        print(img1.shape)
        img = img1
        img[img != 0] = 255  # label use
        plt.subplot(1, 3, 1)
        plt.imshow(img1)
        plt.title('img')
        plt.subplot(1, 3, 2)
        plt.imshow(img, 'gray')
        #plt.show()
        img_name = file.split('.')[0]
        cv2.imwrite(bit8_path + '/' + img_name + '.png', img)


