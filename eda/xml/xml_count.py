import os
from unicodedata import name
import xml.etree.ElementTree as ET
import glob


def count_num(indir):
    # 提取xml文件列表
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    dict = {}  # 新建字典，用于存放各类标签名及其对应的数目
    for i, file in enumerate(annotations):  # 遍历xml文件

        # actual parsing
        in_file = open(file, encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 遍历文件的所有标签
        for obj in root.iter('object'):
            name = obj.find('name').text
            if (name in dict.keys()):
                dict[name] += 1  # 如果标签不是第一次出现，则+1
            else:
                dict[name] = 1  # 如果标签是第一次出现，则将该标签名对应的value初始化为1

    # 打印结果
    print("各类标签的数量分别为：")
    for key in dict.keys():
        print(key + ': ' + str(dict[key]))

if __name__ == '__main__':
    # xml文件所在的目录
    indir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/xml/'
    # 调用函数统计各类标签数目
    count_num(indir)
