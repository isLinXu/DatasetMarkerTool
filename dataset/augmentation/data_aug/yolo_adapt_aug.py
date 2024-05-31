import cv2
import numpy as np
import os
import random
from collections import defaultdict
from pathlib import Path
from typing import Tuple

# 数据增强函数
def random_rotation(image: np.ndarray, angle_range: Tuple[int, int] = (-20, 20)) -> np.ndarray:
    h, w = image.shape[:2]
    angle = random.randint(*angle_range)
    matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    return cv2.warpAffine(image, matrix, (w, h))

def random_flip(image: np.ndarray, horizontal: bool = True, vertical: bool = False) -> Tuple[np.ndarray, int]:
    flip_type = -1
    if horizontal and vertical:
        flip_type = -1
        image = cv2.flip(image, flip_type)
    elif horizontal:
        flip_type = 1
        image = cv2.flip(image, flip_type)
    elif vertical:
        flip_type = 0
        image = cv2.flip(image, flip_type)
    else:
        flip_type = -1
    return image, flip_type

def adjust_bbox(bbox: Tuple[float, float, float, float], img_shape: Tuple[int, int], angle: int, flip_type: int) -> Tuple[float, float, float, float]:
    x, y, w, h = bbox
    img_h, img_w = img_shape

    # Adjust for rotation
    x_center, y_center = x * img_w, y * img_h
    x_center_rotated = (x_center - img_w / 2) * np.cos(np.radians(angle)) - (y_center - img_h / 2) * np.sin(np.radians(angle)) + img_w / 2
    y_center_rotated = (x_center - img_w / 2) * np.sin(np.radians(angle)) + (y_center - img_h / 2) * np.cos(np.radians(angle)) + img_h / 2
    x, y = x_center_rotated / img_w, y_center_rotated / img_h

    # Adjust for flip
    if flip_type == 0:  # Vertical flip
        y = 1 - y
    elif flip_type == 1:  # Horizontal flip
        x = 1 - x
    elif flip_type == -1:  # No flip
        pass

    return x, y, w, h



def random_brightness_contrast(image, brightness_range=(-30, 30), contrast_range=(0.7, 1.3)):
    brightness = random.randint(*brightness_range)
    contrast = random.uniform(*contrast_range)
    return cv2.addWeighted(image, contrast, image, 0, brightness)

def augment_image(image_path: str, label_path: str, output_img_dir: str, output_label_dir: str, num_augmented_images: int) -> None:
    image = cv2.imread(image_path)
    img_h, img_w = image.shape[:2]
    filename = os.path.splitext(os.path.basename(image_path))[0]

    for i in range(num_augmented_images):
        # angle = random.randint(-20, 20)
        angle_range = (-5, 5)
        augmented_image = random_rotation(image, angle_range)
        augmented_image, flip_type = random_flip(augmented_image)
        augmented_image = random_brightness_contrast(augmented_image)

        output_path = os.path.join(output_img_dir, f"{filename}_augmented_{i}.jpg")
        cv2.imwrite(output_path, augmented_image)

        # Adjust the label file.
        output_label_path = os.path.join(output_label_dir, f"{filename}_augmented_{i}.txt")
        with open(label_path, "r") as file:
            lines = file.readlines()
        angle = random.randint(-5, 5)
        with open(output_label_path, "w") as file:
            for line in lines:
                cls, x, y, w, h = map(float, line.split())
                x, y, w, h = adjust_bbox((x, y, w, h), (img_h, img_w), angle, flip_type)
                file.write(f"{int(cls)} {float(x):.6f} {float(y):.6f} {float(w):.6f} {float(h):.6f}\n")

# 数据集增强函数
def augment_dataset(input_img_dir: str, input_label_dir: str, output_img_dir: str, output_label_dir: str,
                        num_augmented_images: int, class_to_augment: int) -> None:
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
def count_labels(input_dir: str) -> defaultdict:
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
def adaptive_augmentation(input_img_dir: str, input_label_dir: str, output_img_dir: str, output_label_dir: str,
                              target_num_samples: int) -> None:
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
    output_img_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output1/images"
    output_label_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output1/labels"
    adaptive_augmentation(input_img_dir, input_label_dir, output_img_dir, output_label_dir, target_num_samples)