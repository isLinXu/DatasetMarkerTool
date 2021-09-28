"""
Script that will create a "dataset" folder with "images" and "labels" sub-folders
These folders will contain pictures from "dataset_extracted" and "dataset_real" folders
"""
import glob, os
import random
import shutil
import logging
import argparse
import sys

def create_dataset(folders, dataset_folder):
    
    
    
    # Percentage of images to be used for the test set
    percentage_test = 10;
    dataset_training_folder = os.path.join(dataset_folder, 'training')
    dataset_testing_folder = os.path.join(dataset_folder, 'testing')
    dataset_training_images_folder = os.path.join(dataset_training_folder, 'images')
    dataset_training_labels_folder = os.path.join(dataset_training_folder, 'labels')
    dataset_testing_images_folder = os.path.join(dataset_testing_folder, 'images')
    dataset_testing_labels_folder = os.path.join(dataset_testing_folder, 'labels')
    
    
    if os.path.isdir(dataset_folder):
        shutil.rmtree(dataset_folder, ignore_errors=True)
    os.makedirs(dataset_training_images_folder, exist_ok=True)
    os.makedirs(dataset_training_labels_folder, exist_ok=True)
    os.makedirs(dataset_testing_images_folder, exist_ok=True)
    os.makedirs(dataset_testing_labels_folder, exist_ok=True)
    
    train_file_number = 0
    test_file_number = 0
    
    for dataset_path in folders:
        
        random.seed(2)
        
        for path_and_filename in glob.iglob(os.path.join(dataset_path, "*.jpg")):  
            file_path, ext = os.path.splitext(path_and_filename)
            
            train_or_test = random.randint(0, 100)
            if train_or_test < percentage_test:
                shutil.copy(path_and_filename, dataset_testing_images_folder)
                shutil.copy(file_path + '.txt', dataset_testing_labels_folder)
                test_file_number += 1
            else:
                shutil.copy(path_and_filename, dataset_training_images_folder)
                shutil.copy(file_path + '.txt', dataset_training_labels_folder)
                train_file_number += 1
                
    logging.info("%d files added to %s" % (train_file_number, dataset_training_folder))
    logging.info("%d files added to %s" % (test_file_number, dataset_testing_folder))
    
if __name__ == '__main__':
    local_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Tool creating dataset folder with structure compatible with yolo project')
    parser.add_argument('folders', nargs='+', help='source folders to include in dataset')
    parser.add_argument('--output', help='Output directory where files will be written', default=local_path + 'dataset')
    
    args = parser.parse_args()
    
    # check folders are valid
    for folder in args.folders:
        if not os.path.isdir(folder):
            logging.error("Folder %s does not exist" % folder)
            sys.exit(1)
            
    create_dataset(args.folders, args.output)
            
            