# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from multiprocessing import Pool
import os.path as osp
import glob
from xml.dom.minidom import Document
from typing import List
import random
import numpy as np
import cv2 as cv
import copy


class CreateImages():
    def __init__(self,obj_dir:str,bg_dir:str,xml_savedir:str,num_process=8):
        self.obj_dir = osp.join(obj_dir)
        self.bg_dir=osp.join(bg_dir)
        self.xml_savedir = osp.join(xml_savedir)
        self.bg_images_repeat=15#重复次数
        self.obj_count=150 #目标数


        obj_images = glob.glob(self.obj_dir + '*.png')
        obj_image_ids = [*map(lambda x: osp.splitext(osp.split(x)[-1])[0], obj_images)]
        self.obj_image_ids = obj_image_ids

        bg_images = glob.glob(self.bg_dir + '*.png')
        bg_image_ids = [*map(lambda x: osp.splitext(osp.split(x)[-1])[0], bg_images)]
        self.bg_image_ids = bg_image_ids

        if not osp.isdir(self.xml_savedir):
            os.makedirs(self.xml_savedir)

        self.num_process = num_process
    
    def _createxml(self,infos:List,savepath:str):
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)

        for i in range(len(infos)):
            #xml_infos : filename,width,height,depth,obj-name,obj-bndbox

            folder = xmlBuilder.createElement("folder")#folder标签
            folderContent = xmlBuilder.createTextNode("folder")
            folder.appendChild(folderContent)
            annotation.appendChild(folder)

            filename = xmlBuilder.createElement("filename")#filename标签
            filenameContent = xmlBuilder.createTextNode(infos[i][0])
            filename.appendChild(filenameContent)
            annotation.appendChild(filename)

            size = xmlBuilder.createElement("size")  # size标签
            width = xmlBuilder.createElement("width")  # size子标签width
            widthContent = xmlBuilder.createTextNode(str(infos[i][1]))
            width.appendChild(widthContent)
            size.appendChild(width)
            height = xmlBuilder.createElement("height")  # size子标签height
            heightContent = xmlBuilder.createTextNode(str(infos[i][2]))
            height.appendChild(heightContent)
            size.appendChild(height)
            depth = xmlBuilder.createElement("depth")  # size子标签depth
            depthContent = xmlBuilder.createTextNode(str(infos[i][3]))
            depth.appendChild(depthContent)
            size.appendChild(depth)
            annotation.appendChild(size)

            object = xmlBuilder.createElement("object")
            picname = xmlBuilder.createElement("name")
            nameContent = xmlBuilder.createTextNode(infos[i][4])
            picname.appendChild(nameContent)

            object.appendChild(picname)
            pose = xmlBuilder.createElement("pose")
            poseContent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(poseContent)

            object.appendChild(pose)
            truncated = xmlBuilder.createElement("truncated")
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)

            object.appendChild(truncated)
            difficult = xmlBuilder.createElement("difficult")
            difficultContent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultContent)

            object.appendChild(difficult)
            bndbox = xmlBuilder.createElement("bndbox")
            xmin = xmlBuilder.createElement("xmin")
            xminContent = xmlBuilder.createTextNode(str(infos[i][5][0]))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)
            ymin = xmlBuilder.createElement("ymin")
            yminContent = xmlBuilder.createTextNode(str(infos[i][5][1]))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)
            xmax = xmlBuilder.createElement("xmax")
            xmaxContent = xmlBuilder.createTextNode(str(infos[i][5][2]))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)
            ymax = xmlBuilder.createElement("ymax")
            ymaxContent = xmlBuilder.createTextNode(str(infos[i][5][3]))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)
            object.appendChild(bndbox)

            annotation.appendChild(object)

        f = open(savepath, 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()
    
    def _cal_iou(self,box1:List, box2:List):
        """
        :param box1: = [xmin1, ymin1, xmax1, ymax1]
        :param box2: = [xmin2, ymin2, xmax2, ymax2]
        :return: 
        """
        xmin1, ymin1, xmax1, ymax1 = box1
        xmin2, ymin2, xmax2, ymax2 = box2
        # 计算每个矩形的面积
        s1 = (xmax1 - xmin1) * (ymax1 - ymin1)  # C的面积
        s2 = (xmax2 - xmin2) * (ymax2 - ymin2)  # G的面积
    
        # 计算相交矩形
        xmin = max(xmin1, xmin2)
        ymin = max(ymin1, ymin2)
        xmax = min(xmax1, xmax2)
        ymax = min(ymax1, ymax2)
    
        w = max(0, xmax - xmin)
        h = max(0, ymax - ymin)
        area = w * h  # C∩G的面积
        iou = area / (s1 + s2 - area+1)
        return iou

    def _createfiles(self,bg_image_ids):
        # 现在传进来的只有图片名没有后缀
        bg_file = osp.join(self.bg_dir,bg_image_ids + '.png')
        random.shuffle(self.bg_image_ids)
        src=cv.imdecode(np.fromfile(bg_file, dtype=np.uint8),cv.IMREAD_UNCHANGED)
        src_h,src_w,_=src.shape
        for i in range(self.bg_images_repeat):
            src_copy=copy.deepcopy(src)
            xml_infos=[]
            add_bbox=[]
            for j in range(self.obj_count):
                obj_path=osp.join(self.obj_dir,self.obj_image_ids[i*self.obj_count+j] + '.png')
                button = cv.imdecode(np.fromfile(obj_path, dtype=np.uint8),cv.IMREAD_UNCHANGED)
                h,w,_=button.shape

                a=1
                while a<300:
                    a=a+1
                    if src_w-w-1 >1 and src_h-h-1 >1:
                        xmin=random.randint(1,src_w-w-1)
                        ymin=random.randint(1,src_h-h-1)
                        xmax=xmin+w
                        ymax=ymin+h
                        c_bbox=[xmin,ymin,xmax,ymax]
                        is_exist=False
                        if len(add_bbox)>0:
                            for p in range(len(add_bbox)):
                                if self._cal_iou(c_bbox,add_bbox[p]) > 0:
                                    is_exist =True
                        
                        if is_exist:
                            continue
                        else:                
                            add_bbox.append(c_bbox)
                            #xml_infos : filename,width,height,depth,obj-name,obj-bndbox
                            file_name=bg_image_ids+'-'+str(i)+'.png'
                            width=src_w
                            height=src_h
                            depth=3
                            obj_name='botton'
                            obj_bndbox=c_bbox
                            info=[file_name,width,height,depth,obj_name,obj_bndbox]
                            xml_infos.append(info)
                            src_copy[ymin:ymin+h,xmin:xmin+w]=button
                            break
                #保存图片
        
            filepath=osp.join(self.xml_savedir,bg_image_ids+'-'+str(i)+'.png')
            flag=cv.imencode(".png",src_copy)[1].tofile(filepath)

            #将对应的xml保存
            filepath2=osp.join(self.xml_savedir,bg_image_ids+'-'+str(i)+'.xml')
            self._createxml(xml_infos,filepath2)

    def run(self):
        with Pool(self.num_process) as p:
            p.map(self._createfiles,self.bg_image_ids)

    def test(self):
        for i in range(10):
            self._createfiles(self.bg_image_ids[i])


if __name__ == "__main__":
    dir="root"
    bg_dir=dir+"/bg/"
    obj_dir=dir+"/button/"
    save_dir=dir+"/mr_result/"

    xml2dota=CreateImages(obj_dir,bg_dir,save_dir)
    xml2dota.run()
    # xml2dota.test()
