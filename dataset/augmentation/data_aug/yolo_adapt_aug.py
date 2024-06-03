import math

import cv2
import numpy as np
import os
import random
from collections import defaultdict
from pathlib import Path
from typing import Tuple, List

from matplotlib import pyplot as plt


def random_rotation(image: np.ndarray, angle_range: Tuple[int, int] = (-20, 20)) -> Tuple[np.ndarray, int]:
    # ... (省略了部分代码)
    h, w = image.shape[:2]
    angle = random.randint(*angle_range)
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    return cv2.warpAffine(image, matrix, (w, h)), angle



def random_crop(image: np.ndarray, label: List[Tuple[int, float, float, float, float]],
                scale_range: Tuple[float, float] = (0.8, 1.0)) -> Tuple[np.ndarray, List[Tuple[int, float, float, float, float]]]:
    h, w = image.shape[:2]
    scale = random.uniform(*scale_range)
    new_h, new_w = int(h * scale), int(w * scale)

    y = random.randint(0, h - new_h)
    x = random.randint(0, w - new_w)

    cropped_image = image[y:y + new_h, x:x + new_w]
    resized_image = cv2.resize(cropped_image, (w, h))

    new_label = []
    for cls, x_center, y_center, width, height in label:
        x_min, y_min = (x_center - width / 2) * w, (y_center - height / 2) * h
        x_max, y_max = (x_center + width / 2) * w, (y_center + height / 2) * h

        x_min_new = np.clip(x_min - x, 0, new_w)
        y_min_new = np.clip(y_min - y, 0, new_h)
        x_max_new = np.clip(x_max - x, 0, new_w)
        y_max_new = np.clip(y_max - y, 0, new_h)

        if x_max_new - x_min_new < 1 or y_max_new - y_min_new < 1:
            continue

        x_center_new = (x_min_new + x_max_new) / 2 / w
        y_center_new = (y_min_new + y_max_new) / 2 / h
        width_new = (x_max_new - x_min_new) / w
        height_new = (y_max_new - y_min_new) / h

        new_label.append((cls, x_center_new, y_center_new, width_new, height_new))

    return resized_image, new_label


def random_flip(image: np.ndarray, horizontal: bool = True, vertical: bool = False) -> Tuple[np.ndarray, int]:
    flip_type = -1 if horizontal and vertical else 1 if horizontal else 0 if vertical else -1
    return cv2.flip(image, flip_type), flip_type

def rotate_points(points, center, angle):
    angle = np.radians(angle)
    rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                           [np.sin(angle), np.cos(angle)]])
    rot_points = np.dot(points - center, rot_matrix) + center
    return rot_points

def adjust_bbox(bbox: Tuple[float, float, float, float], img_shape: Tuple[int, int], angle: int,
                flip_type: int) -> Tuple[float, float, float, float]:
    x, y, w, h = bbox
    img_h, img_w = img_shape

    # Calculate coordinates of the original bbox
    x_min = x * img_w - w * img_w / 2
    y_min = y * img_h - h * img_h / 2
    x_max = x * img_w + w * img_w / 2
    y_max = y * img_h + h * img_h / 2

    # Rotate the bbox
    bbox_points = np.array([[x_min, y_min],
                            [x_min, y_max],
                            [x_max, y_min],
                            [x_max, y_max]])
    center = np.array([img_w / 2, img_h / 2])
    rotated_points = rotate_points(bbox_points, center, angle)
    # Calculate the new bounding box
    x_min_rot, y_min_rot = np.min(rotated_points, axis=0)
    x_max_rot, y_max_rot = np.max(rotated_points, axis=0)

    # Adjust for flip
    if flip_type == 0:  # Vertical flip
        y_min_rot, y_max_rot = img_h - y_max_rot, img_h - y_min_rot
    elif flip_type == 1:  # Horizontal flip
        x_min_rot, x_max_rot = img_w - x_max_rot, img_w - x_min_rot
    elif flip_type == -1:  # No flip
        pass

    # Clip the bbox to be within the image boundaries
    x_min_rot, x_max_rot = np.clip(x_min_rot, 0, img_w), np.clip(x_max_rot, 0, img_w)
    y_min_rot, y_max_rot = np.clip(y_min_rot, 0, img_h), np.clip(y_max_rot, 0, img_h)

    # Calculate the new center, width, and height
    x_center_rot = (x_min_rot + x_max_rot) / 2 / img_w
    y_center_rot = (y_min_rot + y_max_rot) / 2 / img_h
    width_rot = (x_max_rot - x_min_rot) / img_w
    height_rot = (y_max_rot - y_min_rot) / img_h

    return x_center_rot, y_center_rot, width_rot, height_rot


def random_brightness_contrast(image, brightness_range=(-30, 30), contrast_range=(0.7, 1.3)):
    brightness = random.randint(*brightness_range)
    contrast = random.uniform(*contrast_range)
    return cv2.addWeighted(image, contrast, image, 0, brightness)

def bbox_iou(bbox1: Tuple[float, float, float, float], bbox2: Tuple[float, float, float, float]) -> float:
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2
    x1_min, y1_min = x1 - w1 / 2, y1 - h1 / 2
    x1_max, y1_max = x1 + w1 / 2, y1 + h1 / 2
    x2_min, y2_min = x2 - w2 / 2, y2 - h2 / 2
    x2_max, y2_max = x2 + w2 / 2, y2 + h2 / 2

    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(inter_x_max - inter_x_min, 0) * max(inter_y_max - inter_y_min, 0)
    area1 = w1 * h1
    area2 = w2 * h2
    union_area = area1 + area2 - inter_area

    return inter_area / union_area


def random_scale(image: np.ndarray, scale_range: Tuple[float, float] = (0.8, 1.2)) -> np.ndarray:
    h, w = image.shape[:2]
    scale = random.uniform(*scale_range)
    new_h, new_w = int(h * scale), int(w * scale)
    image = cv2.resize(image, (new_w, new_h))
    if scale < 1.0:
        # Need to pad
        pad_h, pad_w = h - new_h, w - new_w
        top, bottom = pad_h // 2, pad_h - (pad_h // 2)
        left, right = pad_w // 2, pad_w - (pad_w // 2)
        return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_REFLECT)
    else:
        # Need to crop
        y, x = (new_h - h) // 2, (new_w - w) // 2
        return image[y:y + h, x:x + w]

def random_noise(image: np.ndarray, intensity: float = 0.05) -> np.ndarray:
    noise = np.random.normal(0, intensity * 255, image.shape)
    return np.clip(image + noise, 0, 255).astype(np.uint8)


def random_perspective(image: np.ndarray, max_ratio: float = 0.1) -> np.ndarray:
    h, w = image.shape[:2]
    shift = max_ratio * min(h, w)
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    pts2 = np.float32([[random.uniform(-shift, shift), random.uniform(-shift, shift)],
                       [w - random.uniform(-shift, shift), random.uniform(-shift, shift)],
                       [random.uniform(-shift, shift), h - random.uniform(-shift, shift)],
                       [w - random.uniform(-shift, shift), h - random.uniform(-shift, shift)]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(image, matrix, (w, h))

def random_occlusion(image: np.ndarray, max_num_rects: int = 3, max_rect_ratio: float = 0.1) -> np.ndarray:
    h, w = image.shape[:2]
    num_rects = random.randint(1, max_num_rects)
    for _ in range(num_rects):
        x = random.randint(0, w)
        y = random.randint(0, h)
        rect_w = random.randint(1, int(w * max_rect_ratio))
        rect_h = random.randint(1, int(h * max_rect_ratio))
        image[y:y + rect_h, x:x + rect_w] = 0
    return image


def augment_image(image_path: str, label_path: str, output_img_dir: str, output_label_dir: str,
                      num_augmented_images: int, iou_threshold: float = 0.5,
                      p_rotation: float = 0.2, p_crop: float = 0.2, p_flip: float = 0.2,
                      p_brightness_contrast: float = 0.2,
                      p_scale: float = 0.2, p_noise: float = 0.2, p_perspective: float = 0.2,
                      p_occlusion: float = 0.2) -> None:
    image = cv2.imread(image_path)
    img_h, img_w = image.shape[:2]
    filename = os.path.splitext(os.path.basename(image_path))[0]

    with open(label_path, 'r') as f:
        label = [tuple(map(float, line.strip().split())) for line in f]

    for i in range(num_augmented_images):
        # Randomly select a transformation based on probabilities
        transformation = random.choices(
            [random_rotation, random_crop, random_flip, random_brightness_contrast, random_scale, random_noise,
             random_perspective, random_occlusion],weights=[p_rotation, p_crop, p_flip, p_brightness_contrast, p_scale, p_noise, p_perspective, p_occlusion])[0]

        # Apply the transformation to the image and label
        if transformation == random_crop:
            augmented_img, label = transformation(image, label)
            angle, flip_type = 0, -1
        elif transformation == random_rotation:
            augmented_img, angle = transformation(image)
            flip_type = -1
        elif transformation == random_flip:
            augmented_img, flip_type = transformation(image)
            angle = 0
        elif transformation == random_crop:
            augmented_img, label = transformation(image, label)
            angle, flip_type = 0, -1
        else:
            augmented_img = transformation(image)
            angle, flip_type = 0, -1

        augmented_label = []
        for bbox in label:
            cls, x, y, w, h = bbox
            x, y, w, h = adjust_bbox((x, y, w, h), (img_h, img_w), angle, flip_type)
            if 0.0 < x < 1.0 and 0.0 < y < 1.0 and w > 0.0 and h > 0.0 and w * img_w >= 1 and h * img_h >= 1:
                augmented_label.append((cls, x, y, w, h))

        with open(os.path.join(output_label_dir, f"{filename}_{i}.txt"), 'w') as f:
            cv2.imwrite(os.path.join(output_img_dir, f"{filename}_{i}.jpg"), augmented_img)
            for cls, x, y, w, h in augmented_label:
                f.write(f"{int(cls)} {x} {y} {w} {h}\n")


def augment_dataset(image_dir: str, label_dir: str, output_img_dir: str, output_label_dir: str,
                    num_augmented_images: int, iou_threshold: float = 0.5) -> None:
    for image_path in Path(image_dir).glob("*.jpg"):
        label_path = Path(label_dir) / (image_path.stem + ".txt")
        augment_image(str(image_path), str(label_path), output_img_dir, output_label_dir, num_augmented_images,
                      iou_threshold)


def count_labels(label_dir: str) -> dict:
    label_count = defaultdict(int)
    for label_path in Path(label_dir).glob("*.txt"):
        with open(label_path, 'r') as f:
            for line in f:
                cls = int(line.strip().split()[0])
                label_count[cls] += 1
    return label_count
def combine_label_counts(count_before: dict, count_after: dict) -> dict:
    combined_count = count_before.copy()
    for cls, count in count_after.items():
        combined_count[cls] += count
    return combined_count

def save_histogram(label_count: dict, title: str, filename: str):
    labels, counts = zip(*label_count.items())
    plt.bar(labels, counts)
    plt.xlabel("Class")
    plt.ylabel("Number of instances")
    plt.title(title)
    plt.savefig(filename)
    plt.close()

def adaptive_augmentation(image_dir: str, label_dir: str, output_img_dir: str, output_label_dir: str,
                          target_samples: int, iou_threshold: float = 0.5) -> None:
    label_count = count_labels(label_dir)
    print("Current label distribution:", label_count)
    num_augmented_images = {cls: math.ceil(target_samples / count) - 1 for cls, count in label_count.items()}
    print(f"Augmenting with {num_augmented_images} additional images per sample")

    for image_path in Path(image_dir).glob("*.jpg"):
        label_path = Path(label_dir) / (image_path.stem + ".txt")
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                cls = int(f.readline().strip().split()[0])
            num_augmented_images_len = math.ceil(target_samples / label_count[cls]) - 1
            print(f"Augmenting class {cls} with {num_augmented_images_len} additional images per sample")
            augment_image(str(image_path), str(label_path), output_img_dir, output_label_dir, num_augmented_images[cls], iou_threshold)


# 主函数
if __name__ == "__main__":
    target_num_samples = 20
    input_img_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/images/train"
    input_label_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/labels/train"
    output_img_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output_0603_2/images"
    output_label_dir = "/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/aug_output_0603_2/labels"

    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    # 在数据增强前保存直方图
    label_count_before = count_labels(input_label_dir)
    save_histogram(label_count_before, "Histogram before data augmentation", "histogram_before.png")
    # 开始数据增强
    adaptive_augmentation(input_img_dir, input_label_dir, output_img_dir, output_label_dir, target_num_samples)
    # 在数据增强后保存直方图
    # 计算增强后的标签数量
    label_count_after = count_labels(output_label_dir)
    label_count_total = combine_label_counts(label_count_before, label_count_after)

    # 在数据增强后保存直方图
    save_histogram(label_count_total, "Histogram after data augmentation", "histogram_after.png")