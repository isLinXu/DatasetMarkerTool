import os
import shutil

if __name__ == '__main__':
    # 原始数据路径(包含所有图片)
    path = '/media/hxzh02/Extreme SSD/无人机输电线路数据集合集/3-无人机航拍输电线路图像'
    # 整理输出路径(汇总所有文件目录下的路径)
    new_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/输电线路航拍数据集'
    # ---------------------------------------------------#
    #   循环遍历路径，复制路径下所有图片文件至输出路径
    # ---------------------------------------------------#
    count = 1
    for root,dirs,files in os.walk(path):
        for i in range(len(files)):
            # 筛选文件以.jpg为后缀
            if(files[i][-3:] == 'jpg' or files[i][-3:] == 'JPG'):
                # 文件路径拼接
                file_path = root + '/' + files[i]
                new_file_path = new_path + '/' + files[i]
                # 复制
                shutil.copy(file_path, new_file_path)
                # shutil.mov(file_path,new_file_path)
                print(count, ':file_path', file_path)
                count += 1

