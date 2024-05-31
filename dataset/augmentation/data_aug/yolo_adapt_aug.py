import cv2
import numpy as np
import os
import random
from collections import defaultdict

# 数据增强函数
def random_rotation(image, angle_range=(-20, 20)):
    h, w = image.shape[:2]
    angle = random.randint(*angle_range)
    matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    return cv2.warpAffine(image, matrix, (w, h))

def random_flip(image, horizontal=True, vertical=False):
    if horizontal:
        image = cv2.flip(image, 1)
    if vertical:
        image = cv2.flip(image, 0)
    return image

def random_brightness_contrast(image, brightness_range=(-30, 30), contrast_range=(0.7, 1.3)):
    brightness = random.randint(*brightness_range)
    contrast = random.uniform(*contrast_range)
    return cv2.addWeighted(image, contrast, image, 0, brightness)

def augment_image(image_path, label_path, output_img_dir, output_label_dir, num_augmented_images):
    image = cv2.imread(image_path)
    filename = os.path.splitext(os.path.basename(image_path))[0]

    for i in range(num_augmented_images):
        augmented_image = random_rotation(image)
        augmented_image = random_flip(augmented_image)
        augmented_image = random_brightness_contrast(augmented_image)

        output_path = os.path.join(output_img_dir, f"{filename}_augmented_{i}.jpg")
        cv2.imwrite(output_path, augmented_image)
        # print(f"Augmented image saved to {output_path}")

        # Copy the label file.
        output_label_path = os.path.join(output_label_dir, f"{filename}_augmented_{i}.txt")
        os.system(f"cp {label_path} {output_label_path}")
        # print(f"Augmented image saved to {output_path}")

# 数据集增强函数
def augment_dataset(input_img_dir, input_label_dir, output_img_dir, output_label_dir, num_augmented_images, class_to_augment):
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    for filename in os.listdir(input_img_dir):
        if filename.endswith(".jpg"):
            image_path = os.path.join(input_img_dir, filename)
            label_path = os.path.join(input_label_dir, filename.replace(".jpg", ".txt"))

            if os.path.exists(label_path):
                with open(label_path, "r") as file:
                    lines = file.readlines()
                    classes = [int(line.split()[0]) for line in lines]

                if class_to_augment in classes:
                    augment_image(image_path, label_path, output_img_dir, output_label_dir, num_augmented_images)

# 计算标签分布
def count_labels(input_dir):
    label_counts = defaultdict(int)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            label_path = os.path.join(input_dir, filename)

            with open(label_path, "r") as file:
                lines = file.readlines()
                classes = [int(line.split()[0]) for line in lines]

                for cls in classes:
                    label_counts[cls] += 1

    return label_counts

# 自适应数据增强
def adaptive_augmentation(input_img_dir, input_label_dir, output_img_dir, output_label_dir, target_num_samples):
    label_counts = count_labels(input_label_dir)
    print("Current label distribution:", label_counts)

    for cls, count in label_counts.items():
        num_augmented_images = (target_num_samples - count) // count
        if num_augmented_images > 0:
            print(f"Augmenting class {cls} with {num_augmented_images} additional images per sample")
            class_to_augment = cls
            augment_dataset(input_img_dir, input_label_dir, output_img_dir, output_label_dir, num_augmented_images, class_to_augment)
        else:
            print(f"Class {cls} has enough samples, no augmentation needed")

# 主函数
if __name__ == "__main__":
    target_num_samples = 10
    input_img_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/images/train"
    input_label_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/labels/train"
    output_img_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output/images"
    output_label_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output/labels"
    adaptive_augmentation(input_img_dir, input_label_dir, output_img_dir, output_label_dir, target_num_samples)