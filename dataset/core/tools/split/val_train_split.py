# -*- coding:utf-8  -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-8-23 上午11:56
@desc: 将数据集划分为train与val

r"""Test Train Split.

This executable is used to split train and test datasets.

Example usage:

    python test_train_split.py \
        --datadir='data/all/' \
        --split=0.1 \
        --train_output='data/train/' \
        --test_output='data/test/' \
        --image_ext='jpeg'

'''
import argparse
import os
from random import shuffle
import pandas as pd
from math import floor
import shutil

from dataset.core.check.check_files import check_dir

parser = argparse.ArgumentParser()
parser.add_argument('--datadir', help='Path to the all input data', type=str)
parser.add_argument('--split', help='Split value - Test %', type=float, default=0.1)
parser.add_argument('--train_output', help='Path to output train data', type=str)
parser.add_argument('--test_output', help='Path to output test data', type=str)
parser.add_argument('--image_ext', help='jpeg or jpg or png', type=str, default='jpeg')
FLAGS = parser.parse_args()

FLAGS.datadir = '/home/hxzh02/文档/datasets_smoke/'
FLAGS.split = 0.1
FLAGS.train_output = '/home/hxzh02/MyGithub/TrainNetHub/Efficient/EfficientDet_master/datasets/smoke_coco/train/'
FLAGS.test_output = '/home/hxzh02/MyGithub/TrainNetHub/Efficient/EfficientDet_master/datasets/smoke_coco/test/'
FLAGS.image_ext = 'jpg'

def get_file_list_from_dir(datadir):
    '''
    从路径中获取文件列表
    :param datadir:
    :return:
    '''
    all_files = os.listdir(os.path.abspath(datadir))
    data_files = list(filter(lambda file: file.endswith('.' + FLAGS.image_ext), all_files))
    shuffled_files = randomize_files(data_files)
    all_cervix_images = pd.DataFrame({'imagepath': shuffled_files})
    all_cervix_images['filename'] = all_cervix_images.apply(lambda row: row.imagepath.split(".")[0], axis=1)
    return all_cervix_images


def randomize_files(file_list):
    '''
    随机获取文件
    :param file_list:
    :return:
    '''
    shuffle(file_list)
    return file_list


def get_training_and_testing_sets(file_list, split):
    '''
    随机分割训练集与测试集
    :param file_list:
    :param split:
    :return:
    '''
    split_index = floor(file_list.shape[0] * split)
    testing = file_list[:split_index]
    training = file_list[split_index:]
    training = training.reset_index(drop=True)
    return training, testing


def write_data(training, testing, datadir, train_output, test_output):
    '''
    将文件数据写入对应路径
    :param training:
    :param testing:
    :param datadir:
    :param train_output:
    :param test_output:
    :return:
    '''
    # Train Data
    print('Writing -', training.shape[0], '- Train data images at -', train_output)
    for name in training['filename']:
        try:
            # Moving xmls
            rd_path = os.path.join(datadir, name + '.xml')

            wr_path = os.path.join(train_output, name + '.xml')
            # shutil.move(rd_path, wr_path)
            shutil.copy(rd_path,wr_path)

            # Moving images
            rd_path = os.path.join(datadir, name + '.' + FLAGS.image_ext)

            wr_path = os.path.join(train_output, name + '.' + FLAGS.image_ext)
            # shutil.move(rd_path, wr_path)
            shutil.copy(rd_path, wr_path)
        except:
            print('Could not find {}'.format(name + '.xml'))

    # Test Data
    print('Writing -', testing.shape[0], '- Test data images at -', test_output)
    for name in testing['filename']:
        try:
            # Moving xmls
            rd_path = os.path.join(datadir, name + '.xml')

            wr_path = os.path.join(test_output, name + '.xml')
            # shutil.move(rd_path, wr_path)
            shutil.copy(rd_path, wr_path)

            # Moving images
            rd_path = os.path.join(datadir, name + '.' + FLAGS.image_ext)

            wr_path = os.path.join(test_output, name + '.' + FLAGS.image_ext)
            # shutil.move(rd_path, wr_path)
            shutil.copy(rd_path, wr_path)
        except:
            print('Could not find {}'.format(name + '.xml'))


def main():
    check_dir(FLAGS.train_output)
    check_dir(FLAGS.test_output)
    file_list = get_file_list_from_dir(FLAGS.datadir)
    print('Read -', file_list.shape[0], '- files from the directory -', FLAGS.datadir)
    training, testing = get_training_and_testing_sets(file_list, FLAGS.split)
    write_data(training, testing, FLAGS.datadir, FLAGS.train_output, FLAGS.test_output)


if __name__ == '__main__':
    main()