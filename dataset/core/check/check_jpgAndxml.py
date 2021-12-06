# -*- coding:utf-8 -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-11-01 上午11:56
@desc: 检查jpeg图片与标注文件是否对应
'''
import os

from tqdm import *

def checkJpgXml(jpeg_dir, annot_dir):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """
    cnt = 0
    error_list = []
    jpeg_dir_list = os.listdir(jpeg_dir)
    for i in tqdm(range(0,len(jpeg_dir_list))):
        # ---------------------------------------------------#
        #   整理分割file信息
        # ---------------------------------------------------#
        file = jpeg_dir_list[i]
        f_name, f_ext = file.split(".")
        # print('f_name', f_name, ',f_ext', f_ext)
        # ---------------------------------------------------#
        #   检查统计对应文件
        # ---------------------------------------------------#
        if not os.path.exists(os.path.join(annot_dir, f_name + ".xml")):
            error_list.append(f_name)
            cnt += 1
    # ---------------------------------------------------#
    #   整理xml信息
    # ---------------------------------------------------#
    print("=====检查完毕=====")
    if cnt > 0:
        print("有%d个文件不符合要求。" % (cnt))
        error_list = sorted(error_list)
        for error in error_list:
            print('error_file', error)
    else:
        print("检查无误：所有图片和对应的xml文件都是一一对应的。")


if __name__ == "__main__":
    # jpeg_dir = r"/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/JPEGImages/"
    # annot_dir = r"/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/Annotations/"
    jpeg_dir = '/media/hxzh02/SB@home/hxzh/Dataset/杆塔倒塌-负样本/src/jpeg/'
    annot_dir = '/media/hxzh02/SB@home/hxzh/Dataset/杆塔倒塌-负样本/src/annotations/'
    checkJpgXml(jpeg_dir, annot_dir)