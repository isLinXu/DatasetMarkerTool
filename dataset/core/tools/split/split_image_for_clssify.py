import os
import random
import shutil
import time


def get_imlist(path):

    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def check_split_move_files(dir_path, img_list, le, mode='train'):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if mode == 'train':
        imgdata = img_list[:le]
    else:
        imgdata = img_list[le:]
    for f in imgdata:
        shutil.move(f, dir_path)
    return 0

def split_create_Data(src_path):
    # 这个文件夹需要提前建好
    train_dir = src_path + 'train/'
    valid_dir = src_path + 'valid/'
    test_dir = src_path + 'test/'
    img_list = get_imlist(src_path)
    count = len(img_list)
    print('count:', count)
    random.shuffle(img_list)
    # 修改划分比例
    le = int(count * 0.8)

    # 划分并移动数据
    check_split_move_files(train_dir, img_list, le, mode='train')
    check_split_move_files(valid_dir, img_list, le, mode='valid')


if __name__ == '__main__':
    start_time = time.time()
    file_path = '/home/hxzh02/图片/coco128/images/train2017/'
    split_create_Data(file_path)
    print('times:',time.time() - start_time)