import os, os.path, sys
import glob
import argparse
import shutil

from xml.etree import ElementTree as ET
from xml.dom import minidom
from shutil import copy


def prettify(CONTENT):
    reparsed = minidom.parseString(CONTENT)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' ' * 4).split('\n') if line.strip()])


def merge_xml(path_to_xml_1, list_path_to_xml_2, new_path):
    # read tree 1
    tree1 = ET.parse(path_to_xml_1)
    root1 = tree1.getroot()
    # read tree 2
    i = 1
    for path_to_xml_2 in list_path_to_xml_2:
        tree2 = ET.parse(path_to_xml_2)
        root2 = tree2.getroot()
        for obj in root2.iter('object'):
            # name.text = nn
            pose = ET.Element('pose')
            pose.text = obj[1].text
            truncated = ET.Element('truncated')
            truncated.text = obj[2].text
            difficult = ET.Element('difficult')
            difficult.text = obj[3].text
            bnbbox = ET.Element('bnbbox')
            xmin = ET.SubElement(bnbbox, 'xmin')
            xmin.text = obj[4][0].text
            ymin = ET.SubElement(bnbbox, 'ymin')
            ymin.text = obj[4][1].text
            xmax = ET.SubElement(bnbbox, 'xmax')
            xmax.text = obj[4][2].text
            ymax = ET.SubElement(bnbbox, 'ymax')
            ymax.text = obj[4][3].text
            root1.insert(6 + i, obj)
            i += 1

    xmlstr = prettify(ET.tostring(root1))
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    name = path_to_xml_1.split("\\")[-1]
    with open(os.path.join(new_path, name), 'w') as f:
        f.write(xmlstr)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-f", "--folder", default="/media/hxzh02/Double/数据集/merge")
    # args.add_argument("-v", "--videoname")
    args = vars(args.parse_args())
    # print(args["folder"])

    list_dirs = os.listdir(args["folder"])
    # print(list_dirs)
    for d in list_dirs:
        print('d', d)
        if os.path.isdir(os.path.join(args["folder"], d)):
            new_path = os.path.join(args["folder"], d, "merged")
            if os.path.exists(new_path):
                shutil.rmtree(new_path)
                os.makedirs(new_path)
            else:
                os.makedirs(new_path)

            ### ----------------- ###
            dir_list = [x[0] for x in os.walk(os.path.join(args["folder"], d))]
            print(dir_list)
            merged_idx = dir_list.index(os.path.join(args["folder"], d, "merged"))
            print('merged_idx', merged_idx)
            dir_list.pop(merged_idx)
            dir_list = dir_list[1:]
            print('dir_list', dir_list)
            # print("///")
            traversed = []
            for folder in dir_list:
                # print(folder)
                for f in glob.glob(str(folder) + "/*.xml"):
                    print(f)
                    shutil.copy(f, os.path.join(new_path, f.split('/')[-1]))

            for i in range(len(dir_list)):
                # for j in range(i+1, len(dir_list)):
                path_1 = dir_list[i]
                list_path_2 = dir_list[i + 1:]
                for f in glob.glob(str(path_1) + "/*.xml"):
                    list_to_merge = []
                    for l in list_path_2:
                        if os.path.exists(os.path.join(l, f.split('/')[-1])):
                            if not f.split('/')[-1] in traversed:
                                f2 = os.path.join(l, f.split('/')[-1])
                                list_to_merge.append(f2)
                                # traversed.append(f.split('\\')[-1])
                        else:
                            if not f.split('/')[-1] in traversed:
                                # traversed.append(f.split('\\')[-1])
                                copy(f, os.path.join(new_path, f.split('/')[-1]))
                    traversed.append(f.split('/')[-1])
                    if len(list_to_merge) != 0:
                        merge_xml(f, list_to_merge, new_path)