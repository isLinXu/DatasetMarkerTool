
import xml.etree.ElementTree as ET
from os import getcwd
classes = ['smoke']
def convert_annotation():
    # in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml' % (year, image_id))
    in_file = '/home/hxzh02/文档/datasets_smoke/smog_train_9248.xml'
    tree = ET.parse(in_file)
    root = tree.getroot()
    if root.find('object') == None:
        return
    # list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg' %(wd, year, image_id))
    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        difficult = 0
        cls = obj.find('name').text
        print(cls)
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),
             int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        # list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

    # list_file.write('\n')

if __name__ == '__main__':
    convert_annotation()