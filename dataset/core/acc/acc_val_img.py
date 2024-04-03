
import os
import glob
import shutil
from tqdm import tqdm
import cv2

def bbox_iou(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    intersection_x_min = max(x1_min, x2_min)
    intersection_y_min = max(y1_min, y2_min)
    intersection_x_max = min(x1_max, x2_max)
    intersection_y_max = min(y1_max, y2_max)

    intersection_area = max(intersection_x_max - intersection_x_min, 0) * max(intersection_y_max - intersection_y_min, 0)
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    union_area = box1_area + box2_area - intersection_area

    return intersection_area / union_area

def parse_yolo_format(line, return_class_id=False):
    values = list(map(float, line.strip().split()))
    if len(values) == 6:
        class_id, x_center, y_center, width, height, _ = values
    else:
        class_id, x_center, y_center, width, height = values

    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2
    if return_class_id:
        return (x_min, y_min, x_max, y_max), class_id
    else:
        return x_min, y_min, x_max, y_max


def draw_bbox(image, bbox, class_id, color=(0, 255, 0), draw_type='pred', thickness=2):
    draw_label = ''
    x_min, y_min, x_max, y_max = bbox
    height, width, _ = image.shape
    x_min, y_min, x_max, y_max = int(x_min * width), int(y_min * height), int(x_max * width), int(y_max * height)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
    draw_label = draw_type + ":" + str(class_id)
    cv2.putText(image, draw_label, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)


def filter_fp_fn_images(prediction_path, ground_truth_path, image_path, root_path, iou_threshold=0.45):
    fp_images = []
    fn_images = []
    tp_images = []
    tn_images = []

    fp_count = 0
    fn_count = 0
    tp_count = 0
    tn_count = 0

    # Get list of file names without extension
    prediction_files = sorted([os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(prediction_path, '*.txt'))])
    ground_truth_files = sorted([os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(ground_truth_path, '*.txt'))])

    # Get list of common file names
    common_files = list(set(prediction_files) & set(ground_truth_files))

    fp_path = root_path + '/FP'
    fn_path = root_path + '/FN'
    tp_path = root_path + '/TP'
    tn_path = root_path + '/TN'

    if not os.path.exists(fp_path):
        os.makedirs(fp_path)

    if not os.path.exists(fn_path):
        os.makedirs(fn_path)

    if not os.path.exists(tp_path):
        os.makedirs(tp_path)

    if not os.path.exists(tn_path):
        os.makedirs(tn_path)

    for file_name in tqdm(common_files, total=len(common_files)):
        pred_file = os.path.join(prediction_path, file_name + '.txt')
        gt_file = os.path.join(ground_truth_path, file_name + '.txt')
        img_file = os.path.join(image_path, file_name + '.jpg')  # Assuming images are in .jpg format

        with open(pred_file, 'r') as pf, open(gt_file, 'r') as gf:
            pred_lines = pf.readlines()
            gt_lines = gf.readlines()

            image = cv2.imread(img_file)
            if image is None:
                # print(f"Warning: Unable to read image {img_file}. Skipping...")
                continue
            fp_detected = False
            fn_detected = False
            for gt_line in gt_lines:
                gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)
                draw_bbox(image, gt_bbox, gt_class_id, color=(0, 255, 0), draw_type='gt')  # Draw ground truth bbox in green

            for pred_line in pred_lines:
                pred_bbox, pred_class_id = parse_yolo_format(pred_line, return_class_id=True)
                draw_bbox(image, pred_bbox, pred_class_id, color=(255, 0, 0), draw_type='pred')  # Draw predicted bbox in red

                max_iou = 0
                for gt_line in gt_lines:
                    gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)
                    iou = bbox_iou(pred_bbox, gt_bbox)
                    max_iou = max(max_iou, iou)

                if max_iou < iou_threshold:
                    if not fp_detected:
                        fp_count += 1
                        fp_detected = True
                    fp_images.append(file_name)
                    cv2.imwrite(os.path.join(fp_path, file_name + '.jpg'), image)
                else:
                    tp_count += 1
                    tp_images.append(file_name)
                    cv2.imwrite(os.path.join(tp_path, file_name + '.jpg'), image)

            for gt_line in gt_lines:
                gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)

                max_iou = 0
                for pred_line in pred_lines:
                    pred_bbox, pred_class_id = parse_yolo_format(pred_line, return_class_id=True)
                    iou = bbox_iou(pred_bbox, gt_bbox)
                    max_iou = max(max_iou, iou)

                if max_iou < iou_threshold:
                    if not fn_detected:
                        fn_count += 1
                        fn_detected = True
                    fn_images.append(file_name)
                    cv2.imwrite(os.path.join(fn_path, file_name + '.jpg'), image)
                else:
                    tn_count += 1
                    tn_images.append(file_name)
                    cv2.imwrite(os.path.join(tn_path, file_name + '.jpg'), image)
    return fp_images, fn_images, tp_images, tn_images, fp_count, fn_count, tp_count, tn_count

if __name__ == '__main__':

    root_path = 'data/test_img/'
    prediction_path = root_path + '/yolov6predictions'
    ground_truth_path = 'datasets_v240402/labels/test'
    image_path = 'datasets_v240402/images/test'

    fp_images, fn_images, tp_images, tn_images, fp_count, fn_count, tp_count, tn_count = filter_fp_fn_images(prediction_path, ground_truth_path, image_path, root_path)

    # 计算Recall、Precision和FAR
    recall = tp_count / (tp_count + fn_count)
    precision = tp_count / (tp_count + fp_count)
    far = fp_count / (fp_count + tn_count)

    print("Recall: {:.2f}".format(recall))
    print("Precision: {:.2f}".format(precision))
    print("FAR: {:.2f}".format(far))

    # print("False Positives:")
    # for fp_image in fp_images:
    #     print(fp_image)

    # print("False Negatives:")
    # for fn_image in fn_images:
    #     print(fn_image)

    # print("True Positives:")
    # for tp_image in tp_images:
    #     print(tp_image)

    # print("True Negatives:")
    # for tn_image in tn_images:
    #     print(tn_image)