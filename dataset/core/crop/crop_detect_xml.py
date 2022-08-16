from PIL import Image
from pylab import *
import os
import xml.etree.ElementTree as ET

from tqdm import tqdm


def _ParseAnnotation(filepath):
    global name, ymin, xmax, xmin, num
    if os.path.exists(anno_path + filepath) == False:
        print(filepath + ' :not found')
    tree = ET.parse(anno_path + filepath)
    # None是一个特殊的空对象，可以用来占位。
    annos = [None] * 500
    num = 0
    for annoobject in tree.iter():
        if 'object' in annoobject.tag:
            for element in list(annoobject):
                if 'name' in element.tag:
                    name = element.text
                if 'bndbox' in element.tag:
                    for size in list(element):
                        if 'xmin' in size.tag:
                            xmin = size.text
                        if 'ymin' in size.tag:
                            ymin = size.text
                        if 'xmax' in size.tag:
                            xmax = size.text
                        if 'ymax' in size.tag:
                            ymax = size.text
                            annos[num] = {'name': name, 'xmin': int(xmin),
                                          'ymin': int(ymin), 'xmax': int(xmax),
                                          'ymax': int(ymax)}

                            num += 1
    return num, annos


def _crop(image_path, crop_path, num, annotation, file, ext='jpg'):
    filenum = os.path.splitext(file)
    filename = filenum[0] + '.' + ext
    if os.path.exists(image_path + filename) != True:
        print(filename + 'not found')
        return
    box = (annotation['xmin'], annotation['ymin'], annotation['xmax'], annotation['ymax'])
    pil_im = Image.open(image_path + filename)

    x_d = annotation['xmax'] - annotation['xmin']
    y_d = annotation['ymax'] - annotation['ymin']
    # 检查box正确性
    if x_d > 0 and y_d > 0:
        print('box:', box, 'x_d:', x_d, 'y_d:', y_d)
        region = pil_im.crop(box)
        pil_region = Image.fromarray(uint8(region))
        pil_region.save(crop_path + annotation['name'] + filenum[0] + '_' + str(num) + '.jpg')
    else:
        print('box check error!')


def crop_from_xml(anno_path, image_path, crop_path, ext):
    '''
    # 将数据集中的标注框从图片中剪裁出来
    Args:
        anno_path: 存放xml文件
        image_path: 存放未剪裁图片
        crop_path: 存放剪裁后图片
    Returns:

    '''
    file_dir_list = os.listdir(anno_path)
    all_annotation = 0
    all_image = 0

    filelist = []
    for file in file_dir_list:
        filelist.append(file)

    # for i in tqdm(range(0, len(filenames))):
    for i in tqdm(range(0, len(filelist))):
        file = filelist[i]
        # for file in filelist:
        num, annos = _ParseAnnotation(file)
        # annotation_num = _crop(num, annos, file)
        # all_annotation = all_annotation + annotation_num
        # all_image+=1
        i = 0
        for j in range(num):
            i += 1
            _crop(image_path, crop_path, i, annos[j], file, ext)
            print(file)
        all_image += 1
    print('all_image:', all_image)


if __name__ == '__main__':
    ####anno_path存放xml文件，image_path存放未剪裁图片，crop_path存放剪裁后图片
    anno_path = '/home/linxu/Desktop/mark_save_1976/VOC2007/Annotations/'
    image_path = '/home/linxu/Desktop/mark_save_1976/VOC2007/JPEGImages/'
    crop_path = '/home/linxu/Desktop/mark_save_1976/crop/'
    ext = 'jpeg'

    crop_from_xml(anno_path, image_path, crop_path, ext)
