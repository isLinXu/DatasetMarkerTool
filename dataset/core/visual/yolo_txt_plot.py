# # !/usr/bin/env python
# # 可视化
# import cv2
# import os
# from tqdm import tqdm
# import random
# import numpy as np
#
# def read_gt(file_path, img_width, img_height):
#     """
#     读取gt的bbox
#     """
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#         boxes = []
#         for line in lines:
#             line = line.strip().split()
#             label = int(line[0])
#             x, y, w, h = map(float, line[1:])
#             x_min = int((x - w / 2) * img_width)
#             y_min = int((y - h / 2) * img_height)
#             x_max = int((x + w / 2) * img_width)
#             y_max = int((y + h / 2) * img_height)
#             boxes.append([x_min, y_min, x_max, y_max, label])
#         return boxes
#
#
# def draw_boxes(img_path, pred_path, class_names):
#     """
#     绘制预测框
#     """
#     img = cv2.imread(img_path)
#     with open(pred_path, "r") as f:
#         lines = f.readlines()
#     boxes = []
#     for line in lines:
#         line = line.strip().split(" ")
#         if len(line) == 6:
#             # vis pred label
#             class_id = int(line[0])
#             confidence = float(line[5])
#             bbox = line[1:5]
#             img_w, img_h = img.shape[1], img.shape[0]
#             # txt里面是【类别，cx,cy,w,h,score】
#             cx, cy, w, h = bbox
#             cx = float(cx)
#             cy = float(cy)
#             w = float(w)
#             h = float(h)
#             x1 = int((cx - w / 2) * img_w)
#             y1 = int((cy - h / 2) * img_h)
#             x2 = int(x1 + w * img_w)
#             y2 = int(y1 + h * img_h)
#             # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
#             # cv2.putText(img, f"{class_names[class_id]}:{confidence:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#             #             (0, 255, 0), 2)
#
#         elif len(line) == 5:
#             # vis gt label
#             label = line[0]
#             label = int(label)
#             x, y, w, h = map(float, line[1:])
#
#             if img is not None:
#                 img_width, img_height = img.shape[1], img.shape[0]
#                 # print("bbox1:",x, y, w, h)
#                 x_min = int((x - w / 2) * img_width)
#                 y_min = int((y - h / 2) * img_height)
#                 x_max = int((x + w / 2) * img_width)
#                 y_max = int((y + h / 2) * img_height)
#                 boxes.append([x_min, y_min, x_max, y_max, label])
#     return img, boxes
#
#
#
# # class_names = ['car', 'ped', 'rider', 'nomotor', 'single_plate', 'forklifts']
# class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
#
# rng = np.random.default_rng(3)
# colors = rng.uniform(0, 255, size=(len(class_names), 3))
#
# def draw_detections(image, boxes, scores, class_ids, mask_alpha=0.3):
#     mask_img = image.copy()
#     det_img = image.copy()
#
#     img_height, img_width = image.shape[:2]
#     size = min([img_height, img_width]) * 0.0006
#     text_thickness = int(min([img_height, img_width]) * 0.001)
#
#     for box, score, class_id in zip(boxes, scores, class_ids):
#         color = colors[class_id]
#         x1, y1, x2, y2 = box.astype(int)
#
#         cv2.rectangle(det_img, (x1, y1), (x2, y2), color, 2)
#         cv2.rectangle(mask_img, (x1, y1), (x2, y2), color, -1)
#
#         label = class_names[class_id]
#         caption = f'{label} {int(score*100)}%'
#         (tw, th), _ = cv2.getTextSize(text=caption, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                                       fontScale=size, thickness=text_thickness)
#         th = int(th * 1.2)
#
#         cv2.rectangle(det_img, (x1, y1), (x1 + tw, y1 - th), color, -1)
#         cv2.rectangle(mask_img, (x1, y1), (x1 + tw, y1 - th), color, -1)
#         cv2.putText(det_img, caption, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), text_thickness, cv2.LINE_AA)
#         cv2.putText(mask_img, caption, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), text_thickness, cv2.LINE_AA)
#
#     return cv2.addWeighted(mask_img, mask_alpha, det_img, 1 - mask_alpha, 0)
#
#
# def draw_boxes_folder(img_folder, pred_folder, class_names, output_folder, pic_nums=None):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#     img_list = os.listdir(img_folder)
#
#     random.shuffle(img_list)
#     if pic_nums is not None:
#         img_list = img_list[:int(pic_nums)]
#     for file in tqdm(img_list):
#         if file.endswith('.jpg') or file.endswith('.png'):
#             img_path = os.path.join(img_folder, file)
#             pred_path = os.path.join(pred_folder, file[:-4] + '.txt')
#             if os.path.exists(pred_path):
#                 img, boxes = draw_boxes(img_path, pred_path, class_names)
#                 if img is not None:
#                     if len(boxes) != 0:
#                         scores = []
#                         class_ids = []
#                         for box in boxes:
#                             x_min, y_min, x_max, y_max, label = box
#                             scores.append(1)  # 假设所有框的置信度为1
#                             class_ids.append(label)
#
#                         img_result = draw_detections(img, np.array(boxes)[:,:4], scores, class_ids)
#                         cv2.imwrite(os.path.join(output_folder, file[:-4] + '_result.jpg'), img_result)
#                     else:
#                         print("pred_path:", pred_path)
#                         with open(pred_path, "r") as f:
#                             lines = f.readlines()
#                             print("lines:", lines)
#
#
#
# if __name__ == '__main__':
#     img_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/images/train2017'
#     pred_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/labels/train2017'
#     output_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/output'
#     draw_boxes_folder(img_folder, pred_folder, class_names, output_folder)


import cv2
import os
from tqdm import tqdm
import random
import numpy as np

class Visualizer:
    def __init__(self, class_names):
        self.class_names = class_names
        self.colors = np.random.default_rng(3).uniform(0, 255, size=(len(class_names), 3))

    @staticmethod
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

    def draw_boxes(self, img_path, pred_path):
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

            elif len(line) == 5:
                # vis gt label
                label = line[0]
                label = int(label)
                x, y, w, h = map(float, line[1:])

                if img is not None:
                    img_width, img_height = img.shape[1], img.shape[0]
                    x_min = int((x - w / 2) * img_width)
                    y_min = int((y - h / 2) * img_height)
                    x_max = int((x + w / 2) * img_width)
                    y_max = int((y + h / 2) * img_height)
                    boxes.append([x_min, y_min, x_max, y_max, label])
        return img, boxes

    def draw_detections(self, image, boxes, scores, class_ids, mask_alpha=0.3):
        mask_img = image.copy()
        det_img = image.copy()

        img_height, img_width = image.shape[:2]
        size = min([img_height, img_width]) * 0.0006
        text_thickness = int(min([img_height, img_width]) * 0.001)

        for box, score, class_id in zip(boxes, scores, class_ids):
            color = self.colors[class_id]
            x1, y1, x2, y2 = box.astype(int)

            cv2.rectangle(det_img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(mask_img, (x1, y1), (x2, y2), color, -1)

            label = self.class_names[class_id]
            caption = f'{label} {int(score*100)}%'
            (tw, th), _ = cv2.getTextSize(text=caption, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                          fontScale=size, thickness=text_thickness)
            th = int(th * 1.2)

            cv2.rectangle(det_img, (x1, y1), (x1 + tw, y1 - th), color, -1)
            cv2.rectangle(mask_img, (x1, y1), (x1 + tw, y1 - th), color, -1)
            cv2.putText(det_img, caption, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255),text_thickness, cv2.LINE_AA)
            cv2.putText(mask_img, caption, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255),
                        text_thickness, cv2.LINE_AA)

        return cv2.addWeighted(mask_img, mask_alpha, det_img, 1 - mask_alpha, 0)

    def draw_boxes_folder(self, img_folder, pred_folder, output_folder, pic_nums=None):
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
                    img, boxes = self.draw_boxes(img_path, pred_path)
                    if img is not None:
                        if len(boxes) != 0:
                            scores = []
                            class_ids = []
                            for box in boxes:
                                x_min, y_min, x_max, y_max, label = box
                                scores.append(1)  # 假设所有框的置信度为1
                                class_ids.append(label)

                            img_result = self.draw_detections(img, np.array(boxes)[:, :4], scores, class_ids)
                            cv2.imwrite(os.path.join(output_folder, file[:-4] + '_result.jpg'), img_result)
                        else:
                            print("pred_path:", pred_path)
                            with open(pred_path, "r") as f:
                                lines = f.readlines()
                                print("lines:", lines)

if __name__ == '__main__':
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    visualizer = Visualizer(class_names)
    img_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/images/train2017'
    pred_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/labels/train2017'
    output_folder = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128/output'
    visualizer.draw_boxes_folder(img_folder, pred_folder, output_folder)