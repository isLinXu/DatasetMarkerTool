# coding: utf-8

from xml.dom.minidom import Document
import os
import cv2
import numpy as np

from numpy.core import unicode
from multiprocessing import Pool


def makexml(txtPath, xmlPath, picPath):  #读取txt路径，xml保存路径，数据集图片所在路径
    if not os.path.exists(xmlPath):
        os.makedirs(xmlPath)
    dict = {
        '0': "button",  #字典对类型进行转换
    }
    files = os.listdir(txtPath)
    for i, name in enumerate(files):
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(txtPath + name, encoding='utf-8')
        txtList = txtFile.readlines()
        filepath = picPath + name[0:-4] + ".png"
        img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        #img = cv2.imread(filepath)
        Pheight, Pwidth, Pdepth = img.shape
        for i in txtList:
            oneline = i.strip().split(" ")
            cla_name = oneline[8]
            x_min, x_max, y_min, y_max = oneline[0], oneline[2], oneline[1], oneline[5]

            folder = xmlBuilder.createElement("folder")  #folder标签
            folderContent = xmlBuilder.createTextNode("folder")
            folder.appendChild(folderContent)
            annotation.appendChild(folder)

            filename = xmlBuilder.createElement("filename")  #filename标签
            filenameContent = xmlBuilder.createTextNode(name[0:-4] + ".png")
            filename.appendChild(filenameContent)
            annotation.appendChild(filename)

            size = xmlBuilder.createElement("size")  # size标签
            width = xmlBuilder.createElement("width")  # size子标签width
            widthContent = xmlBuilder.createTextNode(str(Pwidth))
            width.appendChild(widthContent)
            size.appendChild(width)
            height = xmlBuilder.createElement("height")  # size子标签height
            heightContent = xmlBuilder.createTextNode(str(Pheight))
            height.appendChild(heightContent)
            size.appendChild(height)
            depth = xmlBuilder.createElement("depth")  # size子标签depth
            depthContent = xmlBuilder.createTextNode(str(Pdepth))
            depth.appendChild(depthContent)
            size.appendChild(depth)
            annotation.appendChild(size)

            object = xmlBuilder.createElement("object")
            picname = xmlBuilder.createElement("name")
            nameContent = xmlBuilder.createTextNode(str(cla_name))
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
            mathData = int(x_min)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)
            ymin = xmlBuilder.createElement("ymin")
            mathData = int(y_min)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)
            xmax = xmlBuilder.createElement("xmax")
            mathData = int(x_max)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)
            ymax = xmlBuilder.createElement("ymax")
            mathData = int(y_max)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)
            object.appendChild(bndbox)

            annotation.appendChild(object)

        f = open(xmlPath + name[0:-4] + ".xml", 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()


#makexml("txt所在文件夹","xml保存地址","图片所在地址")
txt_dir = "/txt"
xml_dir = "/xml"
img_dir = "/images"
makexml(txt_dir, xml_dir, img_dir)
