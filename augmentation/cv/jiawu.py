import numpy as np
import cv2 as cv
import os
import random


# file = ['fj.png']
output = 'fj-wu.png'


if __name__ == '__main__':
    file_img = '/home/linxu/Desktop/广西恒信项目/现场图像-中铝智能巡检项目/现场图像/IMG_4550.JPG'
# for file_img in file:
    # 关上图像
    img = cv.imread(file_img)
    mask_img = cv.imread(file_img)

    # 雾的色彩
    mask_img[:, :] = (166, 178, 180)

    # 外面参数可调，次要调整雾的浓度
    image = cv.addWeighted(img,
                           round(random.uniform(0.03, 0.28), 2),
                           mask_img, 1, 0)

    # 保留的文件夹
    cv.imwrite(output, image)