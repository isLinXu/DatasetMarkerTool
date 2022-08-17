import json
import os
# from random import random
import zipfile

import numpy as np

data_parameters = {
    "all_class_sum": 4,  # 分类数
    "src_path": "data//train.zip",  # 原始数据集路径
    "target_path": "/home/data/dataset",  # 要解压的路径
    "data_root_path": "/media/hxzh02/SB@home/hxzh/PaddleDetection_Projects/dataset/meter_cls/",
    "train_list_path": "/media/hxzh02/SB@home/hxzh/PaddleDetection_Projects/dataset/meter_cls/train.txt",
    # train_data.txt路径
    "eval_list_path": "/media/hxzh02/SB@home/hxzh/PaddleDetection_Projects/dataset/meter_cls/val.txt",
    # test_data.txt路径
    "label_dict": {},  # 标签字典
}

def unzip_data(src_path,target_path):

    '''
    解压原始数据集，将src_path路径下的zip包解压至data/dataset目录下
    '''

    if(not os.path.isdir(target_path)):
        z = zipfile.ZipFile(src_path, 'r')
        z.extractall(path=target_path)
        z.close()
    else:
        print("文件已解压")


def create_cls_data_list(data_root_path):
    with open(data_root_path + "val.txt", 'w') as f:
        pass
    with open(data_root_path + "train.txt", 'w') as f:
        pass
    # datapath = data_root_path + '/dataset'
    datapath = data_root_path
    # 所有类别的信息
    class_detail = []
    # 获取所有类别
    class_dirs = os.listdir(datapath)
    # 类别标签
    class_label = 0
    # 获取总类别的名称
    father_paths = datapath.split('/')
    while True:
        if father_paths[len(father_paths) - 1] == '':
            del father_paths[len(father_paths) - 1]
        else:
            break
    father_path = father_paths[len(father_paths) - 1]
    # #存储要写进eval.txt和train.txt中的内容
    train_list = []
    eval_list = []
    all_class_images = 0
    other_file = 0
    # 读取每个类别
    for class_dir in class_dirs:
        if class_dir == 'val.txt' or class_dir == "train.txt" or class_dir == 'readme.json':
            other_file += 1
            continue
        print('正在读取类别：%s' % class_dir)
        # 每个类别的信息
        class_detail_list = {}
        eval_sum = 0
        trainer_sum = 0
        # 统计每个类别有多少张图片
        class_sum = 0
        # 获取类别路径
        # path = datapath + "/" + class_dir
        path = datapath + class_dir
        print('path:', path)
        # 获取所有图片
        img_paths = os.listdir(path)
        for img_path in img_paths:
            # 每张图片的路径
            name_path = path + '/' + img_path
            # 如果不存在这个文件夹,就创建
            if not os.path.exists(datapath):
                os.makedirs(datapath)
            # 每10张图片取一个做测试数据
            if class_sum % 10 == 0:
                eval_sum += 1
                with open(data_root_path + "val.txt", 'a') as f:
                    eval_list.append(name_path + "\t%d" % class_label + "\n")
            else:
                trainer_sum += 1
                with open(data_root_path + "train.txt", 'a') as f:
                    train_list.append(name_path + "\t%d" % class_label + "\n")
            class_sum += 1
            all_class_images += 1
        # 说明的json文件的class_detail数据
        class_detail_list['class_name'] = class_dir
        class_detail_list['class_label'] = class_label
        class_detail_list['class_eval_images'] = eval_sum
        class_detail_list['class_trainer_images'] = trainer_sum
        class_detail.append(class_detail_list)
        class_label += 1
    # 获取类别数量
    all_class_sum = len(class_dirs) - other_file
    data_parameters['all_class_sum'] = all_class_sum
    # 乱序
    path1 = data_root_path + "val.txt"
    path2 = data_root_path + "train.txt"

    print('eval_list', eval_list)
    # random.shuffle(eval_list)

    np.random.seed(12)
    np.random.shuffle(eval_list)

    with open(path1, 'a') as f:
        for eval_image in eval_list:
            f.write(eval_image)
    # 乱序
    np.random.shuffle(train_list)
    with open(path2, 'a') as f2:
        for train_image in train_list:
            f2.write(train_image)

    # 说明的json文件信息
    readjson = {}
    readjson['all_class_name'] = father_path
    readjson['all_class_sum'] = all_class_sum
    readjson['all_class_images'] = all_class_images
    readjson['class_detail'] = class_detail
    jsons = json.dumps(readjson, sort_keys=True, indent=4, separators=(',', ': '))
    with open(data_root_path + '/' + "readme.json", 'w') as f:
        f.write(jsons)
    print('图像列表已生成')

if __name__ == '__main__':
    '''
    参数初始化
    '''
    src_path = data_parameters['src_path']
    target_path = data_parameters['target_path']
    train_list_path = data_parameters['train_list_path']
    data_root_path = data_parameters['data_root_path']
    eval_list_path = data_parameters['eval_list_path']


    '''
    解压原始数据到指定路径
    '''
    # unzip_data(src_path, target_path)


    '''
    划分训练集与验证集，乱序，生成数据列表
    '''
    # 每次生成数据列表前，首先清空train.txt和eval.txt
    with open(train_list_path, 'w') as f:
        f.seek(0)
        f.truncate()
    with open(eval_list_path, 'w') as f:
        f.seek(0)
        f.truncate()

    # 生成数据列表
    create_cls_data_list(data_root_path)