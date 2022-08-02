r"""Test Train Split.
This executable is used to split train and test datasets.
Example usage:
    python test_train_split.py \
        --datadir='data/all/' \
        --split=0.1 \
        --train_output='data/train/' \
        --test_output='data/test/' \
        --image_ext='jpeg'
"""

import argparse
import os
from random import shuffle
import pandas as pd
from math import floor
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--datadir', help='Path to the all input data', type=str)
parser.add_argument('--split', help='Split value - Test %', type=float, default=0.1)
parser.add_argument('--train_output', help='Path to output train data', type=str)
parser.add_argument('--test_output', help='Path to output test data', type=str)
parser.add_argument('--image_ext', help='jpeg or jpg or png', type=str, default='jpeg')
FLAGS = parser.parse_args()

FLAGS.datadir = '/home/hxzh02/图片/coco128/ALL/'
FLAGS.split = 0.2
FLAGS.train_output = '/home/hxzh02/图片/coco128/train_data/'
FLAGS.test_output = '/home/hxzh02/图片/coco128/val_data/'
FLAGS.image_ext = 'jpg'


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Creating directory -', directory)
    else:
        print('Directory exists -', directory)


def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    data_files = list(filter(lambda file: file.endswith('.' + FLAGS.image_ext), all_files))
    shuffled_files = randomize_files(data_files)
    all_cervix_images = pd.DataFrame({'imagepath': shuffled_files})
    all_cervix_images['filename'] = all_cervix_images.apply(lambda row: row.imagepath.split(".")[0], axis=1)
    return all_cervix_images


def randomize_files(file_list):
    shuffle(file_list)
    return file_list


def get_training_and_testing_sets(file_list, split):
    split_index = floor(file_list.shape[0] * split)
    testing = file_list[:split_index]
    training = file_list[split_index:]
    training = training.reset_index(drop=True)
    return training, testing


def write_data(training, testing, datadir, train_output, test_output):
    # Train Data
    print('Writing -', training.shape[0], '- Train data images at -', train_output)
    for name in training['filename']:
        try:
            # Moving xmls
            rd_path = os.path.join(datadir, name + '.xml')

            wr_path = os.path.join(train_output, name + '.xml')
            shutil.move(rd_path, wr_path)

            # Moving images
            rd_path = os.path.join(datadir, name + '.' + FLAGS.image_ext)

            wr_path = os.path.join(train_output, name + '.' + FLAGS.image_ext)
            shutil.move(rd_path, wr_path)
        except:
            print('Could not find {}'.format(name + '.xml'))

    # Test Data
    print('Writing -', testing.shape[0], '- Test data images at -', test_output)
    for name in testing['filename']:
        try:
            # Moving xmls
            rd_path = os.path.join(datadir, name + '.xml')

            wr_path = os.path.join(test_output, name + '.xml')
            shutil.move(rd_path, wr_path)

            # Moving images
            rd_path = os.path.join(datadir, name + '.' + FLAGS.image_ext)

            wr_path = os.path.join(test_output, name + '.' + FLAGS.image_ext)
            shutil.move(rd_path, wr_path)
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