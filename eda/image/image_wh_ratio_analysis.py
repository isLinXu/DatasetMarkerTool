import os
from unicodedata import name
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import glob

def ratio(indir):
    # 提取xml文件列表
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')
    # count_0, count_1, count_2, count_3 = 0, 0, 0, 0 # 举反例，不要这么写
    count = [0 for i in range(20)]

    for i, file in enumerate(annotations): # 遍历xml文件
        # actual parsing
        in_file = open(file, encoding = 'utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 遍历文件的所有检测框
        for obj in root.iter('object'):
            xmin = obj.find('bndbox').find('xmin').text
            ymin = obj.find('bndbox').find('ymin').text
            xmax = obj.find('bndbox').find('xmax').text
            ymax = obj.find('bndbox').find('ymax').text
            Aspect_ratio = (int(ymax)-int(ymin)) / (int(xmax)-int(xmin))
            if int(Aspect_ratio/0.25) < 19:
                count[int(Aspect_ratio/0.25)] += 1
            else:
                count[-1] += 1
    sign = [0.25*i for i in range(20)]
    plt.bar(x=sign, height=count)
    plt.show()
    print(count)

if __name__ == '__main__':
    # xml文件所在的目录
    indir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/xml'
    ratio(indir)

