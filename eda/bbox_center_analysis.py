import os
from unicodedata import name
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import glob


def distribution(indir):
    '''
    检测框中心分布分析
    画一个检测框中心分布散点图，直观地反应检测框中心点在图像中的位置分布。
    Args:
        indir:

    Returns:

    '''
    # 提取xml文件列表
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')
    data_x, data_y = [], []

    for i, file in enumerate(annotations):  # 遍历xml文件
        # actual parsing
        in_file = open(file, encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()
        width = int(root.find('size').find('width').text)
        height = int(root.find('size').find('height').text)

        # 遍历文件的所有检测框
        for obj in root.iter('object'):
            xmin = int(obj.find('bndbox').find('xmin').text)
            ymin = int(obj.find('bndbox').find('ymin').text)
            xmax = int(obj.find('bndbox').find('xmax').text)
            ymax = int(obj.find('bndbox').find('ymax').text)
            x = (xmin + (xmax - xmin)) / width
            y = (ymin + (ymax - ymin)) / height
            data_x.append(x)
            data_y.append(y)

    plt.scatter(data_x, data_y, s=1, alpha=0.1)
    plt.show()


if __name__ == '__main__':
    in_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/xml'
    distribution(in_dir)