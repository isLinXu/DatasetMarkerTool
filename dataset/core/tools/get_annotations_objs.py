"""
Features:
1. Get the target in the yolo xml annotation file
2. Get the background image after removing the target
"""

import os.path as osp
import glob
import cv2
import os
import numpy as np
import copy
import xml.etree.ElementTree as ET
from multiprocessing import Pool



classes=["button",'person','nonmotor']

class GetAnnotationsObjs():
    def __init__(self,img_dir,xml_dir,save_bg_dir,save_obj_dir,classes,num_process=8):
        self.img_dir=img_dir
        self.xml_dir=xml_dir
        self.save_obj_dir=save_obj_dir
        self.save_bg_dir=save_bg_dir
        xmls=glob.glob(xml_dir+"*.xml")
        xml_ids=[*map(lambda x:osp.splitext(osp.split(x)[-1])[0],xmls)]
        self.xml_ids=xml_ids
        self.classes=classes
        self.num_process = num_process

        if not osp.isdir(self.save_obj_dir):
            os.makedirs(self.save_obj_dir)
        if not osp.isdir(self.save_bg_dir):
            os.makedirs(self.save_bg_dir)
        for i in range(len(self.classes)):
            cls_dir=osp.join(self.save_obj_dir,self.classes[i])
            if not osp.isdir(cls_dir):
                os.makedirs(cls_dir)

    def getannotations(self,xml_ids):
        xmfile_path=osp.join(self.xml_dir,xml_ids+".xml")
        imagefile_path=osp.join(self.img_dir,xml_ids+".png")
        if os.path.isfile(imagefile_path):
            image = cv2.imdecode(np.fromfile(imagefile_path, dtype=np.uint8),cv2.IMREAD_UNCHANGED)
            bg_imagepath=osp.join(self.save_bg_dir,xml_ids+".png")
            result_img=copy.deepcopy(image)

            tree = ET.parse(xmfile_path)
            root = tree.getroot()
            global object_id
            object_id=0
            for obj in root.iter('object'):
                object_id+=1
                # difficult=obj.find('difficult').text
                cls=obj.find('name').text
                if cls in self.classes:
                    xmlbox = obj.find('bndbox')
                    # b是每个Object中，一个bndbox上下左右像素的元组
                    x_start = int(xmlbox.find('xmin').text)
                    x_end= int(xmlbox.find('xmax').text)
                    y_start=int(xmlbox.find('ymin').text)
                    y_end=int(xmlbox.find('ymax').text)
                    crop_img=image[y_start:y_end,x_start:x_end]
                    save_path=osp.join(self.save_obj_dir,str(cls),xml_ids+"_"+str(object_id)+".png")
                    cv2.imencode(".png",crop_img)[1].tofile(save_path)
                    #将obj区域用左上角像素值填充
                    pixel_value=result_img[y_start,x_start]
                    result= result_img[y_start:y_end,x_start:x_end]
                    result[::]=pixel_value
        
            cv2.imencode(".png",result_img)[1].tofile(bg_imagepath)

    def run(self):
        with Pool(self.num_process) as p:
            p.map(self.getannotations,self.xml_ids)


if __name__ == '__main__':
    root_dir="root"
    images_dir=root_dir+'/images/'
    xml_dir=root_dir+'/xml/'
    save_bg_dir=root_dir+'/bg/'
    save_obj_dir=root_dir+'/objs/'
    anno=GetAnnotationsObjs(images_dir,xml_dir,save_bg_dir,save_obj_dir,classes)
    anno.run()