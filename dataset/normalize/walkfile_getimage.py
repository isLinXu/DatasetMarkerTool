# -*- coding:utf-8  -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-12-24 上午09:56
@desc: 归一化从图片数据目录下遍历文件
'''

import os
import shutil

from tqdm import tqdm

def normalize_walkfile(path, new_path):
    # ---------------------------------------------------#
    #   循环遍历路径，复制路径下所有图片文件至输出路径
    # ---------------------------------------------------#
    count = 1
    for root, dirs, files in os.walk(path):
        for i in tqdm(range(0, len(files))):
            # 筛选文件以.jpg为后缀
            if (files[i][-3:] == 'jpg' or files[i][-3:] == 'JPG' or files[i][-3:] == 'png'):
                # 文件路径拼接
                file_path = root + '/' + files[i]
                new_file_path = new_path + '/' + files[i]
                # 复制
                shutil.copy(file_path, new_file_path)
                # shutil.mov(file_path,new_file_path)
                print(count, ':file_path', file_path)
                count += 1




if __name__ == '__main__':
    # 原始数据路径(包含所有图片)
    # path = '/home/hxzh02/文档/deep-learning-for-image-processing/pytorch_classification/Test3_vggnet/data_set/flower_data/'
    path = '/media/hxzh02/SB@home/hxzh/Dataset/PPLTA航拍输电线路数据集/data_original_size/'
    # 整理输出路径(汇总所有文件目录下的路径)
    # new_path = '/home/hxzh02/文档/deep-learning-for-image-processing/pytorch_classification/Test3_vggnet/data_set/flower_data/'
    new_path = '/media/hxzh02/SB@home/hxzh/Dataset/PPLTA航拍输电线路数据集/data_original_size/'

    # 调用函数
    normalize_walkfile(path, new_path)



