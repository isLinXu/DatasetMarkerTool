
import cv2
import os
from utils.fileHelper import os_mkdir

def images_Normalization(path, size = (640,480), img_show=True):
    """
    图像数据归一化
    :param path:
    :param img_show:
    :return:
    """
    for root, dirs, files in os.walk(path):
        print('################################################################')
        for name in files:
            if len(dirs) == 0:
                fname = os.path.join(root, name)
                print('fname', fname)
                print('name', name)
                # 处理原图img
                src = cv2.imread(fname)
                src = cv2.resize(src, size)
                src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
                if img_show:
                    cv2.imshow('src_img', src)
                    k = cv2.waitKey() & 0xff
                    if k == 27: return 0
                # 创建src目录并存储图片
                src_dir = root + '/src/'
                src_path = root + name
                # print('src_dir', src_dir)
                # print('src_path', src_path)
                # os_mkdir(src_dir)
                cv2.imwrite(src_path, src)

if __name__ == '__main__':
    img_path = '/home/hxzh02/文档/PokeGAN/data/sprites_rgb'
    images_Normalization(img_path, size = (96,96), img_show=True)