
import os
import random as rnd
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', help='The path where all the images are stored', type=str)
parser.add_argument('--train_percentage', help='Percentage of dataset for training', type=float, default=0.8)
FLAGS = parser.parse_args()

folder_names = os.listdir(FLAGS.image_folder)

if not os.path.isdir("Splitted_images/test"):
    os.makedirs("Splitted_images/test")
if not os.path.isdir("Splitted_images/train"):
    os.makedirs("Splitted_images/train")

def move_files(dic, train_or_test):
    for key in  dic.keys():
        for file_path in dic[key]:
            shutil.move(os.path.join(FLAGS.image_folder, key, file_path), os.path.join('Splitted_images', train_or_test, file_path))

def main():
    FILE_TRAIN = {}
    FILE_TEST = {}
    XML_TRAIN = {}
    XML_TEST = {}
    for folder in folder_names:
        all_images = os.listdir(os.path.join(FLAGS.image_folder, folder))
        images_jpg = [image for image in all_images if image.endswith('jpg')]
        images_xml = [image for image in all_images if image.endswith('xml')]
        index = [i for i, label in enumerate(images_jpg)]
        images_jpg.sort()
        images_xml.sort()
        rnd.seed(230)
        rnd.shuffle(index)
        split = int(FLAGS.train_percentage * len(images_jpg))
        FILE_TRAIN[folder] = [images_jpg[idx] for idx in index[:split]]
        FILE_TEST[folder] = [images_jpg[idx] for idx in index[split:]]
        XML_TRAIN[folder] = [images_xml[idx] for idx in index[:split]]
        XML_TEST[folder] = [images_xml[idx] for idx in index[split:]]
    move_files(FILE_TRAIN, 'train')
    move_files(XML_TRAIN, 'train')
    move_files(FILE_TEST, 'test')
    move_files(XML_TEST, 'test')

if __name__ == '__main__':
    main()