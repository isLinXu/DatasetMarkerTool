
import os
from unicodedata import name
import xml.etree.ElementTree as ET
import glob

def Image_size(indir):
    # 提取xml文件列表
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')
    width_heights = []

    for i, file in enumerate(annotations): # 遍历xml文件
        # actual parsing
        in_file = open(file, encoding = 'utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()
        width = int(root.find('size').find('width').text)
        height = int(root.find('size').find('height').text)
        print('(width, height):', (width, height))
        if [width, height] not in width_heights: width_heights.append([width, height])

    print("数据集中，有{}种不同的尺寸，分别是：".format(len(width_heights)))
    for item in width_heights:
        print(item)


if __name__ == '__main__':
    # xml文件所在的目录
    indir='/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/xml'
    Image_size(indir)
