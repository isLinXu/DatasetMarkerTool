

import math
import cv2
import os
from tqdm import tqdm
import random

from dataset.core.visual.yolo_txt_plot import draw_boxes_folder


def merge_images_in_grid(image_folder, output_folder, grid_size=(2, 2), img_size=(416, 416)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img_list = os.listdir(image_folder)
    random.shuffle(img_list)

    num_images = grid_size[0] * grid_size[1]
    for i in tqdm(range(0, len(img_list), num_images), desc="Merging images in grids"):
        grid_images = []
        for r in range(grid_size[0]):
            row_images = []
            for c in range(grid_size[1]):
                idx = i + r * grid_size[1] + c
                if idx < len(img_list):
                    img_path = os.path.join(image_folder, img_list[idx])
                    img = cv2.imread(img_path)
                    if img is not None:
                        img_resized = cv2.resize(img, img_size)
                        row_images.append(img_resized)
            if len(row_images) > 0:
                row_image = cv2.hconcat(row_images)
                grid_images.append(row_image)

        if len(grid_images) > 0:
            grid_image = cv2.vconcat(grid_images)
            output_path = os.path.join(output_folder, f"grid_{i // num_images + 1}.jpg")
            cv2.imwrite(output_path, grid_image)

def merge_images_in_grid(image_folder, output_folder, grid_size=(2, 2), img_size=(416, 416)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img_list = os.listdir(image_folder)
    random.shuffle(img_list)

    num_images = grid_size[0] * grid_size[1]
    for i in tqdm(range(0, len(img_list), num_images), desc="Merging images in grids"):
        grid_images = []
        for r in range(grid_size[0]):
            row_images = []
            for c in range(grid_size[1]):
                idx = i + r * grid_size[1] + c
                if idx < len(img_list):
                    img_path = os.path.join(image_folder, img_list[idx])
                    img = cv2.imread(img_path)
                    if img is not None:  # Check if the image is not None
                        img_resized = cv2.resize(img, img_size)
                        row_images.append(img_resized)
            if len(row_images) > 0:
                row_image = cv2.hconcat(row_images)
                grid_images.append(row_image)

        if len(grid_images) > 0:
            grid_image = cv2.vconcat(grid_images)
            output_path = os.path.join(output_folder, f"grid_{i // num_images + 1}.jpg")
            cv2.imwrite(output_path, grid_image)


def merge_images_in_batchsize_grid(image_folder, output_folder, batch_size=4, img_size=(416, 416)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img_list = os.listdir(image_folder)
    random.shuffle(img_list)

    grid_size = int(math.sqrt(batch_size))

    for i in tqdm(range(0, len(img_list), batch_size), desc="Merging images in grids"):
        grid_images = []
        for r in range(grid_size):
            row_images = []
            for c in range(grid_size):
                idx = i + r * grid_size + c
                if idx < len(img_list):
                    img_path = os.path.join(image_folder, img_list[idx])
                    img = cv2.imread(img_path)
                    if img is not None:  # Check if the image is not None
                        img_resized = cv2.resize(img, img_size)
                        row_images.append(img_resized)
            if len(row_images) > 0:
                row_image = cv2.hconcat(row_images)
                grid_images.append(row_image)

        if len(grid_images) > 0:
            grid_image = cv2.vconcat(grid_images)
            output_path = os.path.join(output_folder, f"grid_{i // batch_size + 1}.jpg")
            cv2.imwrite(output_path, grid_image)


if __name__ == "__main__":
    # Example usage:
    img_folder = 'datasets/images/test'
    pred_folder = 'datasets/labels/test'
    output_folder = 'datasets/model_labels_test/'
    class_names = ['nomotor', 'bike']

    draw_boxes_folder(img_folder, pred_folder, class_names, output_folder)

    batch_size = 36
    img_size = (416, 416)
    merge_images_in_batchsize_grid(output_folder, output_folder + "bs_grids", batch_size, img_size)