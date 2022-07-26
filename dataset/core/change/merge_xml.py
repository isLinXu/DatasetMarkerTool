from xml.etree.ElementTree import ElementTree, Element, parse
import xml.etree.ElementTree as ET
import os
import shutil

# 格式化
from dataset.core.check.check_files import check_dir_bool


def __indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def merge_annotations(hole_path, arm_path, out_path):
    '''
    合并同名标注文件，融合多目标对象
    :param hole_path: 标注文件路径1
    :param arm_path:  目标标注文件路径2
    :param out_path:  合并输出文件路径3 => 2->1
    :return:
    '''
    if check_dir_bool(hole_path) and check_dir_bool(arm_path) and check_dir_bool(out_path):
        for hole_xml in os.listdir(hole_path):
            # 将同名xml合并
            if os.path.exists(os.path.join(arm_path, hole_xml)):
                print('fusing', hole_xml)
                tree_hole = parse(os.path.join(hole_path, hole_xml))
                root_hole = tree_hole.getroot()  # annotation

                new_hole = tree_hole

                tree_arm = parse(os.path.join(arm_path, hole_xml))
                root_arm = tree_arm.getroot()  # annotation
                object = (tree_arm.findall('object'))
                for i in range(len(object)):
                    root_hole.append(object[i])
                __indent(root_hole)
                new_hole.write(os.path.join(out_path, hole_xml))
            # 不同名xml复制
            else:
                print('copying', hole_xml)
                shutil.copy(os.path.join(hole_path, hole_xml), out_path)

            # 将不同名xml复制
            for arm_xml in os.listdir(arm_path):
                if not os.path.exists(os.path.join(out_path, arm_xml)):
                    print('copying')
                    shutil.copy(os.path.join(arm_path, arm_xml), out_path)
    else:
        print('path not exist')


if __name__ == '__main__':
    hole_path = '/home/linxu/Desktop/test/merge/'
    arm_path = '/home/linxu/Desktop/test/merge2/'
    out_path = '/home/linxu/Desktop/test/mergeall/'
    merge_annotations(hole_path, arm_path, out_path)
