# -*- coding:utf-8  -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-11-24 上午12:56
@desc: 数据集处理为YOLO格式
'''

import xml.etree.ElementTree as ET
import pickle
import os
from glob import glob
from os import listdir, getcwd
from os.path import join
import random
from shutil import copyfile

# 分类类别
# classes = ["nest", "trash", "kite", "balloon"] # 异物分类
# classes = ["insulator", "defect"]              # 绝缘子分类
# classes = ['smoke']                            # 烟雾检测
# classes = ["head", "person", "helmet"]         # 安全帽检测
# classes = ['fire', 'smoke']                    # 烟火检测
# classes = ['tower_body','tower_head','tower_foot','tower_body_down'] # 杆塔检测

from tqdm import tqdm

# 塔头检测
# classes = ['tower_head', 'tower_head_defect']
# classes = ['tower_body', 'tower_body_down', 'tower_body_lean']
classes = ['insulator', 'breakage', 'defect']
# 塔身检测
# classes = ['tower_body', 'tower_body_defect']
# classes = ['tower_body','tower_head','tower_foot','tower_body_down',
#            'insulator', 'defect',
#            'line','line_break','line_extract',
#            'nest', 'trash', 'kite', 'balloon',
#            ]
# classes = ['tower_body','tower_head','tower_foot','tower_body_down',
#            'insulator', 'defect',
#            'line','line_break','line_extract',
#            'nest', 'trash', 'kite', 'balloon',
#            'fire', 'smoke']

# 划分训练集比率
TRAIN_RATIO = 90

def clear_hidden_files(path):
    '''
    清除目录下隐藏文件
    :param path:
    :return:
    '''
    dir_list = os.listdir(path)
    for i in dir_list:
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith("._"):
                os.remove(abspath)
        else:
            clear_hidden_files(abspath)


def convert(size, box):
    '''
    转换格式
    :param size:
    :param box:
    :return:
    '''
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

classlist = []
def convert_annotation(dir_path, dataset_name, image_id):
    '''
    转换annotation
    :param image_id:
    :return:
    '''
    in_file = open(dir_path + dataset_name + '/VOC2007/Annotations/%s.xml' % image_id)
    out_file = open(dir_path + dataset_name + '/VOC2007/YOLOLabels/%s.txt' % image_id, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        classlist.append(cls)
        if len(classes) > 1:
            difficult = obj.find('difficult').text
            if cls not in classes or int(difficult) == 1:
                continue

        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))

        # 避免由于w或h为0造成的convert带来的错误
        if w != 0 and h!= 0:
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    # 整理object类别列表
    classdd = list(set(classlist))
    print('classlist', classdd)
    in_file.close()
    out_file.close()


def trans_prepare_config(dir_path='data/', dataset_name='VOCdevkit_xxx'):
    data_base_dir = os.path.join(dir_path + dataset_name + "/")
    if not os.path.isdir(data_base_dir):
        os.mkdir(data_base_dir)
    print('data_base_dir', data_base_dir)
    work_sapce_dir = os.path.join(data_base_dir, "VOC2007/")
    if not os.path.isdir(work_sapce_dir):
        os.mkdir(work_sapce_dir)
    annotation_dir = os.path.join(work_sapce_dir, "Annotations/")
    if not os.path.isdir(annotation_dir):
        os.mkdir(annotation_dir)
    clear_hidden_files(annotation_dir)
    image_dir = os.path.join(work_sapce_dir, "JPEGImages/")
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    clear_hidden_files(image_dir)
    yolo_labels_dir = os.path.join(work_sapce_dir, "YOLOLabels/")
    if not os.path.isdir(yolo_labels_dir):
        os.mkdir(yolo_labels_dir)
    clear_hidden_files(yolo_labels_dir)
    yolov5_images_dir = os.path.join(data_base_dir, "images/")
    if not os.path.isdir(yolov5_images_dir):
        os.mkdir(yolov5_images_dir)
    clear_hidden_files(yolov5_images_dir)
    yolov5_labels_dir = os.path.join(data_base_dir, "labels/")
    if not os.path.isdir(yolov5_labels_dir):
        os.mkdir(yolov5_labels_dir)
    clear_hidden_files(yolov5_labels_dir)
    yolov5_images_train_dir = os.path.join(yolov5_images_dir, "train/")
    if not os.path.isdir(yolov5_images_train_dir):
        os.mkdir(yolov5_images_train_dir)
    clear_hidden_files(yolov5_images_train_dir)
    yolov5_images_test_dir = os.path.join(yolov5_images_dir, "val/")
    if not os.path.isdir(yolov5_images_test_dir):
        os.mkdir(yolov5_images_test_dir)
    clear_hidden_files(yolov5_images_test_dir)
    yolov5_labels_train_dir = os.path.join(yolov5_labels_dir, "train/")
    if not os.path.isdir(yolov5_labels_train_dir):
        os.mkdir(yolov5_labels_train_dir)
    clear_hidden_files(yolov5_labels_train_dir)
    yolov5_labels_test_dir = os.path.join(yolov5_labels_dir, "val/")
    if not os.path.isdir(yolov5_labels_test_dir):
        os.mkdir(yolov5_labels_test_dir)
    clear_hidden_files(yolov5_labels_test_dir)

    print('dir_path', dir_path)
    train_file = open(dir_path + "yolov5_train.txt", 'w')
    test_file = open(dir_path + "yolov5_val.txt", 'w')
    train_file.close()
    test_file.close()
    train_file = open(os.path.join(dir_path + "yolov5_train.txt"), 'a')
    test_file = open(os.path.join(dir_path + "yolov5_val.txt"), 'a')
    list_imgs = os.listdir(image_dir)  # list image files
    prob = random.randint(1, 100)

    for i in tqdm(range(0, len(list_imgs))):
        path = os.path.join(image_dir, list_imgs[i])
        if os.path.isfile(path):
            image_path = image_dir + list_imgs[i]
            voc_path = list_imgs[i]
            (nameWithoutExtention, extention) = os.path.splitext(os.path.basename(image_path))
            (voc_nameWithoutExtention, voc_extention) = os.path.splitext(os.path.basename(voc_path))
            annotation_name = nameWithoutExtention + '.xml'
            annotation_path = os.path.join(annotation_dir, annotation_name)
            label_name = nameWithoutExtention + '.txt'
            label_path = os.path.join(yolo_labels_dir, label_name)
        prob = random.randint(1, 100)
        print('file:', annotation_name, '|', "Probability: %d" % prob)

        # 训练集
        if (prob < TRAIN_RATIO):
            if os.path.exists(annotation_path):
                train_file.write(image_path + '\n')
                # 转换label
                # print('nameWithoutExtention',nameWithoutExtention)
                convert_annotation(dir_path=dir_path, dataset_name=dataset_name, image_id=nameWithoutExtention)
                copyfile(image_path, yolov5_images_train_dir + voc_path)
                copyfile(label_path, yolov5_labels_train_dir + label_name)
        else:
            # 测试集
            if os.path.exists(annotation_path):
                test_file.write(image_path + '\n')
                # 转换label
                convert_annotation(dir_path=dir_path, dataset_name=dataset_name, image_id=nameWithoutExtention)
                copyfile(image_path, yolov5_images_test_dir + voc_path)
                copyfile(label_path, yolov5_labels_test_dir + label_name)

    print('classlist', classlist)
    train_file.close()
    test_file.close()


if __name__ == '__main__':
    # 设置数据集根目录路径
    # dir_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/7-输电线路绝缘子数据集VOC/'
    # dir_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/5-安全帽数据集5000张/'
    # dir_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/'
    dir_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/'
    # 设置数据集名称
    # dataset_name = 'dataset_insulator'
    # dataset_name = 'dataset_safetyHat'
    # dataset_name = 'VOCdevkit_towerhead_detect'
    # dataset_name = 'VOCdevkit_towerbody_detect'
    # dataset_name = 'VOCdevkit_towerbody_detect'
    dataset_name = 'VOCdevkit_Insulator_datasets'
    trans_prepare_config(dir_path, dataset_name)
