
# -*-coding:utf-8-*-
import os
import shutil
from os import listdir

from dataset.core.check.check_files import check_dir

dataset_path = '/home/hxzh02/文档/datasets_smoke/'
train_dir = '/home/hxzh02/文档/datasets_smoke/train/'
test_dir = '/home/hxzh02/文档/datasets_smoke/test/'
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
    print('file', file_name)
    # 以 _ 分割提取类别号
    classOrder = str(file_name.split('_')[0])
    # 以第二个 _ 分割验证与测试集
    sdata = file_name.split('_')[1:]
    if sdata:
        type_d = sdata[0]
        if type_d == 'train':
            print('type:', type_d)
            rd_path = os.path.join(dataset_path, file_name + '.jpg')
            check_dir(train_dir)
            wr_path = os.path.join(train_dir, file_name + '.jpg')
            shutil.copy(rd_path, wr_path)
        else:
            print('type:', type_d)
            check_dir(test_dir)
            wr_path = os.path.join(test_dir, file_name + '.jpg')
            shutil.copy(rd_path, wr_path)
    # print(sdata,type_d)

    labelList.append(classOrder)
    fileList.append(file_name)
print(labelList)
print(fileList)
