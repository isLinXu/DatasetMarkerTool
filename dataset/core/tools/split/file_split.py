
# -*-coding:utf-8-*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-8-23 上午11:56
@desc: 对按照特定方式以字符拼接成的数据集进行划分
例如: smog_train_17683.jpg
     smog_test_8268.xml
     可按照_与.对其进行字符分割来进行区分
'''
import os
import shutil
from os import listdir

from dataset.core.check.check_files import check_dir

dataset_path = '/home/hxzh02/文档/call-phone_datasets/'
train_dir = '/home/hxzh02/文档/call-phone_datasets/train/'
test_dir = '/home/hxzh02/文档/call-phone_datasets/test/'
# 类标签列表
labelList = []
fileList = []
typeList = []
datasetList = listdir(dataset_path)
print(datasetList)
# 文件夹中文件数量
datasetLength = len(datasetList)
for i in range(datasetLength):
    # 获取文件名字符串
    filename = datasetList[i]
    # 以 . 分割提取文件名
    file_name = filename.split('.')[0]
    # print('file', file_name)
    # 以 _ 分割提取类别号
    classOrder = str(file_name.split('_')[0])
    # 以第二个 _ 分割验证与测试集
    sdata = file_name.split('_')[1:]
    if sdata:
        type_d = sdata[0]
        if type_d == 'train':
            rd_jpg_path = os.path.join(dataset_path, file_name + '.jpg')
            wr_jpg_path = os.path.join(train_dir, file_name + '.jpg')
            rd_xml_path = os.path.join(dataset_path, file_name + '.xml')
            wr_xml_path = os.path.join(train_dir, file_name + '.xml')
            check_dir(train_dir)

            shutil.copy(rd_jpg_path, wr_jpg_path)
            shutil.copy(rd_xml_path, wr_xml_path)
        else:
            rd_jpg_path = os.path.join(dataset_path, file_name + '.jpg')
            wr_jpg_path = os.path.join(test_dir, file_name + '.jpg')
            rd_xml_path = os.path.join(dataset_path, file_name + '.xml')
            wr_xml_path = os.path.join(test_dir, file_name + '.xml')
            check_dir(test_dir)

            shutil.copy(rd_jpg_path, wr_jpg_path)
            shutil.copy(rd_xml_path, wr_xml_path)
        print('write jpg:', wr_jpg_path)
        print('write xml:', wr_xml_path)

    labelList.append(classOrder)
    fileList.append(file_name)
# print(labelList)
# print(fileList)
