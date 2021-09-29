# -*- coding: utf-8 -*-
##Count the total number of targets of training samples in yolo's xml

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


total_object=0 #total obj  count
def calc_total_objcount(xml_dir):

    files=os.listdir(xml_dir)
    for image_add in files:
        in_file = open(xml_dir + image_add,'rb')
        tree = ET.parse(in_file)
        root = tree.getroot()
        # 在一个XML中每个Object的迭代
        for obj in root.iter('object'):
            global total_object
            total_object=total_object+1

    print("obj count:",total_object)


if __name__ == "__main__":
    xml_dir=""
    calc_total_objcount(xml_dir)