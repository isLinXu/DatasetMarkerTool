import cv2
import os

import numpy as np
from tqdm import tqdm

from utils.fileHelper import os_mkdir

def check_dir(directory):
    '''
    检查路径
    :param directory:
    :return:
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Creating directory -', directory)
    else:
        print('Directory exists -', directory)

def images_Normalization(path, size=(640, 480), rotate=0, color_space=0, img_show=True):
    """
    图像数据归一化
    :param path:
    :param img_show:
    :return:
    """
    global src
    for root, dirs, files in os.walk(path):
        for i in tqdm(range(0, len(files))):
            name = files[i]
            if len(dirs) == 0:
                fname = os.path.join(root, name)
                print('fname', fname)
                print('name', name)

                # 处理原图img
                img_src = cv2.imread(fname)

                # resize调整大小
                if size != (0, 0):
                    src = cv2.resize(img_src, size)

                # 旋转角度逆时针rotate=0,1,2,3
                src = np.rot90(img_src, rotate)

                # 修改颜色空间
                if color_space != 0:
                    # src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
                    src = cv2.cvtColor(src, color_space)

                if img_show:
                    cv2.imshow('src_img', src)
                    k = cv2.waitKey() & 0xff
                    if k == 27: return 0
                # 创建dst目录并存储图片
                src_dir = root + '/dst/'
                check_dir(src_dir)
                src_path = src_dir + name
                cv2.imwrite(src_path, src)


if __name__ == '__main__':
    img_path = '/home/linxu/Desktop/20220319电表采集/电表流水线0/'
    color_space = 0
    # color_space = cv2.COLOR_RGB2BGR
    rotate = 3
    images_Normalization(path=img_path, size=(0, 0),
                         rotate=rotate, color_space=color_space,
                         img_show=False)
