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

    intersection_area = max(intersection_x_max - intersection_x_min, 0) * max(intersection_y_max - intersection_y_min,
                                                                              0)
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

    # Initialize dictionaries to store counts for each class
    fp_count = {}
    fn_count = {}
    tp_count = {}
    tn_count = {}

    prediction_files = sorted(
        [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(prediction_path, '*.txt'))])
    ground_truth_files = sorted(
        [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(ground_truth_path, '*.txt'))])

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
        img_file = os.path.join(image_path, file_name + '.jpg')

        with open(pred_file, 'r') as pf, open(gt_file, 'r') as gf:
            pred_lines = pf.readlines()
            gt_lines = gf.readlines()

            image = cv2.imread(img_file)
            if image is None:
                continue

            for gt_line in gt_lines:
                gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)
                draw_bbox(image, gt_bbox, gt_class_id, color=(0, 255, 0), draw_type='gt')

            for pred_line in pred_lines:
                pred_bbox, pred_class_id = parse_yolo_format(pred_line, return_class_id=True)
                draw_bbox(image, pred_bbox, pred_class_id, color=(255, 0, 0), draw_type='pred')

                max_iou = 0
                for gt_line in gt_lines:
                    gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)
                    iou = bbox_iou(pred_bbox, gt_bbox)
                    max_iou = max(max_iou, iou)

                if max_iou < iou_threshold:
                    if pred_class_id not in fp_count:
                        fp_count[pred_class_id] = 0
                    fp_count[pred_class_id] += 1

                    # Create class-specific folder if it doesn't exist
                    class_fp_path = os.path.join(fp_path, str(pred_class_id))
                    if not os.path.exists(class_fp_path):
                        os.makedirs(class_fp_path)

                    fp_images.append(file_name)
                    cv2.imwrite(os.path.join(class_fp_path, file_name + '.jpg'), image)
                else:
                    if pred_class_id not in tp_count:
                        tp_count[pred_class_id] = 0
                    tp_count[pred_class_id] += 1

                    # Create class-specific folder if it doesn't exist
                    class_tp_path = os.path.join(tp_path, str(pred_class_id))
                    if not os.path.exists(class_tp_path):
                        os.makedirs(class_tp_path)

                    tp_images.append(file_name)
                    cv2.imwrite(os.path.join(class_tp_path, file_name + '.jpg'), image)

            for gt_line in gt_lines:
                gt_bbox, gt_class_id = parse_yolo_format(gt_line, return_class_id=True)

                max_iou = 0
                for pred_line in pred_lines:
                    pred_bbox, pred_class_id = parse_yolo_format(pred_line, return_class_id=True)
                    iou = bbox_iou(pred_bbox, gt_bbox)
                    max_iou = max(max_iou, iou)

                if max_iou < iou_threshold:
                    if gt_class_id not in fn_count:
                        fn_count[gt_class_id] = 0
                    fn_count[gt_class_id] += 1

                    # Create class-specific folder if it doesn't exist
                    class_fn_path = os.path.join(fn_path, str(gt_class_id))
                    if not os.path.exists(class_fn_path):
                        os.makedirs(class_fn_path)

                    fn_images.append(file_name)
                    cv2.imwrite(os.path.join(class_fn_path, file_name + '.jpg'), image)
                else:
                    if gt_class_id not in tn_count:
                        tn_count[gt_class_id] = 0
                    tn_count[gt_class_id] += 1

                    # Create class-specific folder if it doesn't exist
                    class_tn_path = os.path.join(tn_path, str(gt_class_id))
                    if not os.path.exists(class_tn_path):
                        os.makedirs(class_tn_path)

                    tn_images.append(file_name)
                    cv2.imwrite(os.path.join(class_tn_path, file_name + '.jpg'), image)

    return fp_images, fn_images, tp_images, tn_images, fp_count, fn_count, tp_count, tn_count

def calculate_metrics(tp_count, fn_count, fp_count, tn_count, num_classes):
    recall = {}
    precision = {}
    far = {}

    for class_id in range(num_classes):
        tp = tp_count.get(class_id, 0)
        fn = fn_count.get(class_id, 0)
        fp = fp_count.get(class_id, 0)
        tn = tn_count.get(class_id, 0)

        # Print counts
        print(f"Class {class_id}: TP = {tp}, FN = {fn}, FP = {fp}, TN = {tn}")
        if tp + fn != 0:
            recall[class_id] = tp / (tp + fn)
        else:
            recall[class_id] = None

        if tp + fp != 0:
            precision[class_id] = tp / (tp + fp)
        else:
            precision[class_id] = None

        if fp + tn != 0:
            far[class_id] = fp / (fp + tn)
        else:
            far[class_id] = None

    return recall, precision, far


def main():
    root_path = 'datasets_v240402_04_01_large_infer'
    prediction_path = root_path + '/yolov6predictions'
    ground_truth_path = 'datasets_v240402/labels/test'
    image_path = 'datasets_v240402/images/test'

    fp_images, fn_images, tp_images, tn_images, fp_count, fn_count, tp_count, tn_count = filter_fp_fn_images(
        prediction_path, ground_truth_path, image_path, root_path)

    num_classes = 2
    recall, precision, far = calculate_metrics(tp_count, fn_count, fp_count, tn_count, num_classes)

    # Print results
    for class_id in recall.keys():
        print(f"Class {class_id}: Recall = {recall[class_id]}, Precision = {precision[class_id]}, FAR = {far[class_id]}")


if __name__ == "__main__":
    main()