# coding=utf-8
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-11-04 下午16:24
@desc: 遍历文件夹,根据后缀文件类型划分文件
'''
import os
import shutil


def files_split_data(path_files):
    # 读取指定文件夹中的所有文件,并将文件夹中所有的文件名字存入变量files_list中
    files_list = os.listdir(path_files)

    # 文件夹中所有文件的数目，并打印文件数目
    num_files = len(files_list)
    print(str(num_files) + '个文件')

    # 遍历所有文件
    for file in files_list:
        type = os.path.splitext(file)[1]  # 获取文件的类型

        # 根据文件类型设置路径
        if type == '.xml':
            type = 'Annotations'
        elif type == '.jpg':
            type = 'JPEGImages'

        # 给新建文件夹路径
        type_path = os.path.join(path_files, type)

        '''
        建立文件夹，并防止重复建立；复制文件到指定文件夹中；
        判断文件夹中是否有该文件，若有则跳过，若没有则写入文件夹
        '''
        if os.path.isdir(type_path):
            print(file)
            new_file = os.path.join(type_path, file)  # 给遍历到的文件路径
            if os.path.exists(new_file):  # 判断文件路径有没有，有则跳过，没有则将其写入到文件夹
                continue
            else:
                shutil.copyfile(os.path.join(path_files, file), os.path.join(type_path, file))
        else:
            os.mkdir(type_path)
            shutil.copyfile(os.path.join(path_files, file), os.path.join(type_path, file))

if __name__ == '__main__':
    # 指定文件夹路径
    path_files = r'/home/hxzh02/文档/datasets_smoke/'
    files_split_data(path_files)

