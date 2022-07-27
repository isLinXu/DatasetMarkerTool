import os
import shutil

#按照VOC数据集Main文件夹下的txt文件将测试集图片分离出来
test_path = '/home/omnisky/project/tf-faster-rcnn/data/VOCdevkit2007/VOC2007/ImageSets/Main/test.txt'
anno_path = '/home/omnisky/project/tf-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/'
new_path = '/home/omnisky/project/tf-faster-rcnn/data/VOCdevkit2007/VOC2007/testimages/'

def _main():
    fp = open(test_path, 'r')
    xml_list = fp.readlines()
    fp.close()
    i = 0
    for file in xml_list:
        xml_file = file.replace('\n', '')
        shutil.copyfile(anno_path + xml_file+'.jpg', new_path + xml_file+'.jpg')
        i =+ 1
        print (xml_file+'.jpg')
    print (i)

if __name__ == '__main__':
    _main()
