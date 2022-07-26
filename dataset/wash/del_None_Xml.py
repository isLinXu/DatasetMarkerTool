import os
import xml.etree.ElementTree as ET

def clear_None_xml(anno_path,DELNUM=0):
    '''
    删除数据集中空的xml文件
    Args:
        anno_path: xml文件路径
        DELNUM: 删除个数，默认为0

    Returns:

    '''
    filelist = os.listdir(anno_path)
    all_annotation = 0
    all_image = 0
    for file in filelist:
        _DelNoneAnnotation(file,anno_path)
    print(DELNUM)


def _DelNoneAnnotation(filepath,anno_path):
    if os.path.exists(anno_path + filepath) == False:
        print(filepath + ' :not found')
    tree = ET.parse(anno_path + filepath)
    num = 0
    for annoobject in tree.iter():
        if 'object' in annoobject.tag:
            num += 1
    if num == 0:
        os.remove(anno_path + filepath)
        print(filepath)
        global DELNUM
        DELNUM += 1


if __name__ == '__main__':
    anno_path = '/home/linxu/Desktop/annotaions/'
    DELNUM = 0
    clear_None_xml(anno_path)
