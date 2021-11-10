import os
from os import listdir, getcwd
from os.path import join
import shutil

def get_files(inPath,out_pic_Path,out_xml_path):     
    for filepath,dirnames,filenames in os.walk(inPath):   #在多级目录下找文件 
        for filename in filenames:
            str1 = filename.split('.')[0]
            str1_1 = filename.split('.')[1]
            if str1_1 == "xml":
                shutil.copy(filepath + "/" + filename, out_xml_path)
            elif str1_1 == "jpg" or str1_1 == "jpeg" or str1_1 == "JPG" or str1_1 == "JPEG":
                shutil.copy(filepath + "/" + filename, out_pic_Path) #复制文件
                #shutil.move() 移动文件  
            else:
                continue

if __name__ == '__main__':
    in_path = r"D:\wjy\train_12_classes\datas\Illegal_umbrella\video_image"  # 输入需要复制里面内容的文件夹路径
    out_pic_Path = r"D:\wjy\train_12_classes\datas\Illegal_umbrella\data1\pic"  # 将找到的图片放到该路径里
    out_xml_path = r"D:\wjy\train_12_classes\datas\Illegal_umbrella\data1\label"  # 将找到的xml文件放到该路径里
    get_files(in_path,out_pic_Path,out_xml_path)