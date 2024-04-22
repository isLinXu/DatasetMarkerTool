import os
import os.path
import glob


def os_mkdir(path):
    '''
    目录创建/操作函数
    :param path:
    :return:
    '''
    # 去除首位空格
    path = path.strip()
    # 去除尾部/符号
    path = path.rstrip("/")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

import os
import json
from tqdm import tqdm

def get_files_in_directory(dir_path):
    files_dict = {}
    for root, dirs, files in tqdm(os.walk(dir_path)):
        files_dict[root] = files
    return files_dict

def save_to_json(data, json_file):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

# dir_path = '/path/to/your/directory'  # Replace with your directory path
# json_file = '/path/to/your/json/file'  # Replace with your json file path
#
# files_dict = get_files_in_directory(dir_path)
# save_to_json(files_dict, json_file)

def trans_endwith_lower_upper(realpath,mode='lower'):
    # 将图片jpg文件后缀小写或者大写
    extension = 'JPG'
    file_list = glob.glob(realpath + '*.' + extension)
    for root, dirs, files in os.walk(realpath):
        print(root, dirs, files)
        for file in files:
            fname = file.split('.')[0]
            fend = file.split('.')[1]
            if mode == 'lower':
                fend = fend.lower()
            elif mode == 'upper':
                fend = fend.upper()
            print('fend', fend)

            file_path = os.path.join(root, file)
            trans_path = root + fname + '.' + fend
            os.rename(file_path, trans_path)

if __name__ == '__main__':
    realpath = '/home/linxu/Desktop/JPG/'
    trans_endwith_lower_upper(realpath, mode='upper')
