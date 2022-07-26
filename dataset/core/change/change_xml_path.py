##修改xml文件中的<path>，与实际数据路径对应
##author:leo

# coding=utf-8
import os
import os.path
import xml.dom.minidom

xml_file_path = '/media/hxzh02/SB@home/hxzh/Dataset/11-5电塔照片视频/照片/annotaions'
jpeg_file_path = '/media/hxzh02/SB@home/hxzh/Dataset/11-5电塔照片视频/照片/'
files = os.listdir(xml_file_path)  # 得到文件夹下所有文件名称
s = []
for xmlFile in files:  # 遍历文件夹
    if not os.path.isdir(xmlFile):  # 判断是否是文件夹,不是文件夹才打开
        print(xmlFile)
        # xml文件读取操作
        # 将获取的xml文件名送入到dom解析
        # ---------------------------------------------------#
        #   最核心的部分,路径拼接,输入的是具体路径
        # ---------------------------------------------------#
        dom = xml.dom.minidom.parse(os.path.join(xml_file_path, xmlFile))
        root = dom.documentElement
        # 获取标签对path之间的值
        original_path = root.getElementsByTagName('path')
        folder_name = root.getElementsByTagName('folder')
        # 原始信息
        p0 = original_path[0]
        f0 = folder_name[0]

        path0 = p0.firstChild.data  # 原始路径
        fname0 = f0.firstChild.data
        print('path0', path0, 'fname0',fname0)
        # 修改
        if path0.find("\\"):
            jpg_name = path0.split('\\')[-1]  # 获取图片名
            fold_name = jpeg_file_path
        else:
            jpg_name = path0.split('/')[-1]  # 获取图片名
            fold_name = xml_file_path.split('/')[-1]
        print('jpg_name', jpg_name)
        print('fold_name', fold_name)



        modify_path = xml_file_path + '/' + jpg_name  # 修改后path
        print('file_path:', xml_file_path)
        p0.firstChild.data = modify_path
        f0.firstChild.data = fold_name

        # 保存修改到xml文件中
        with open(os.path.join(xml_file_path, xmlFile), 'w') as fh:
            dom.writexml(fh)
            print('修改path OK!')
