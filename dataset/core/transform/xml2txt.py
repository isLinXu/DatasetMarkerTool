import xml.etree.ElementTree as ET
from os import getcwd
#-------------------------------------#
# 解析xml文件，voc2yolov4.py划分的比例
# 生成训练集、验证集、测试集路径.txt文件
#-------------------------------------#
sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

wd = getcwd()
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
# classes = ["Wheat"]


def convert_annotation(year, image_id, list_file):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml' % (year, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    if root.find('object') == None:
        return
    list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg' %
                    (wd, year, image_id))
    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        difficult = 0
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),
             int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a)
                                        for a in b]) + ',' + str(cls_id))

    list_file.write('\n')


for year, image_set in sets:
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt' %
                     (year, image_set)).read().strip().split()
    list_file = open('trainTxt/%s_%s.txt' % (year, image_set), 'w')
    for image_id in image_ids:
        convert_annotation(year, image_id, list_file)
    list_file.close()
