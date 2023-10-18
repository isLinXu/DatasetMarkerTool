# !/usr/bin/env python
# 可视化
import cv2
import os
from tqdm import tqdm
import random


def read_gt(file_path, img_width, img_height):
    """
    读取gt的bbox
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        boxes = []
        for line in lines:
            line = line.strip().split()
            label = int(line[0])
            x, y, w, h = map(float, line[1:])
            x_min = int((x - w / 2) * img_width)
            y_min = int((y - h / 2) * img_height)
            x_max = int((x + w / 2) * img_width)
            y_max = int((y + h / 2) * img_height)
            boxes.append([x_min, y_min, x_max, y_max, label])
        return boxes


def draw_boxes(img_path, pred_path, class_names):
    """
    绘制预测框
    """
    img = cv2.imread(img_path)
    with open(pred_path, "r") as f:
        lines = f.readlines()
    boxes = []
    for line in lines:
        line = line.strip().split(" ")
        if len(line) == 6:
            # vis pred label
            class_id = int(line[0])
            confidence = float(line[5])
            bbox = line[1:5]
            img_w, img_h = img.shape[1], img.shape[0]
            # txt里面是【类别，cx,cy,w,h,score】
            cx, cy, w, h = bbox
            cx = float(cx)
            cy = float(cy)
            w = float(w)
            h = float(h)
            x1 = int((cx - w / 2) * img_w)
            y1 = int((cy - h / 2) * img_h)
            x2 = int(x1 + w * img_w)
            y2 = int(y1 + h * img_h)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(img, f"{class_names[class_id]}:{confidence:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

        elif len(line) == 5:
            # vis gt label
            label = line[0]
            label = int(label)
            x, y, w, h = map(float, line[1:])

            if img is not None:
                img_width, img_height = img.shape[1], img.shape[0]
                # print("bbox1:",x, y, w, h)
                x_min = int((x - w / 2) * img_width)
                y_min = int((y - h / 2) * img_height)
                x_max = int((x + w / 2) * img_width)
                y_max = int((y + h / 2) * img_height)
                boxes.append([x_min, y_min, x_max, y_max, label])
    return img, boxes


def draw_boxes_folder(img_folder, pred_folder, class_names, output_folder, pic_nums=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    img_list = os.listdir(img_folder)

    random.shuffle(img_list)
    if pic_nums is not None:
        img_list = img_list[:int(pic_nums)]
    for file in tqdm(img_list):
        if file.endswith('.jpg') or file.endswith('.png'):
            img_path = os.path.join(img_folder, file)
            pred_path = os.path.join(pred_folder, file[:-4] + '.txt')
            if os.path.exists(pred_path):
                # print("sss")
                img, boxes = draw_boxes(img_path, pred_path, class_names)
                if img is not None:
                    if len(boxes) != 0:
                        for box in boxes:
                            x_min, y_min, x_max, y_max, label = box
                            print("box:", box)
                            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                            cv2.putText(img, 'gt_' + str(class_names[label]), (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 255, 0), 2)
                        cv2.imwrite(os.path.join(output_folder, file[:-4] + '_result.jpg'), img)
                    else:
                        print("pred_path:", pred_path)
                        with open(pred_path, "r") as f:
                            lines = f.readlines()
                            print("lines:", lines)


if __name__ == '__main__':
    img_folder = 'datasets/images/test'
    pred_folder = 'datasets/labels/test'
    output_folder = 'datasets/model_labels_test/'
    class_names = ['nomotor', 'bike']
    draw_boxes_folder(img_folder, pred_folder, class_names, output_folder)