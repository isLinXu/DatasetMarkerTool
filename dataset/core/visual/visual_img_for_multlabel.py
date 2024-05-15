import os
import cv2
from tqdm import tqdm


def read_txt(txt_path, img_width, img_height):
    '''
    读取txt文件并将其转化为array
    Args:
        txt_path:   txt文件路径
        img_width:  图片宽度
        img_height: 图片高度
    Returns:
    '''
    try:
        with open(txt_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {txt_path}")
        return []
    bboxes = []
    for line in lines:
        try:
            cls, x_center, y_center, width, height = list(map(float, line.strip().split()))
            xmin = int((x_center - width / 2) * img_width)
            ymin = int((y_center - height / 2) * img_height)
            xmax = int((x_center + width / 2) * img_width)
            ymax = int((y_center + height / 2) * img_height)
            bboxes.append([int(cls), xmin, ymin, xmax, ymax])
        except Exception as e:
            print(f"Error processing line: {line}, error: {e}")
    return bboxes


def draw_bboxes(image, bboxes, label_names, color=(255, 0, 0)):
    '''
    绘制图片上的bbox
    Args:
        image:  图片
        bboxes: bbox列表
        label_names: 类别名称列表
        color: bbox颜色
    Returns:
    '''
    img = image.copy()
    for bbox in bboxes:
        cls, *coords = bbox
        label = label_names[cls]
        cv2.rectangle(img, (coords[0], coords[1]), (coords[2], coords[3]), color, 2)
        cv2.putText(img, label, (coords[0], coords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return img


# 计算IoU
def calculate_iou(bbox1, bbox2):
    '''
    计算两个bbox的IoU
    Args:
        bbox1:
        bbox2:

    Returns:
    '''
    xmin1, ymin1, xmax1, ymax1 = bbox1
    xmin2, ymin2, xmax2, ymax2 = bbox2
    inter_xmin = max(xmin1, xmin2)
    inter_ymin = max(ymin1, ymin2)
    inter_xmax = min(xmax1, xmax2)
    inter_ymax = min(ymax1, ymax2)
    inter_area = max(inter_xmax - inter_xmin, 0) * max(inter_ymax - inter_ymin, 0)
    area1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    area2 = (xmax2 - xmin2) * (ymax2 - ymin2)
    union_area = area1 + area2 - inter_area
    return inter_area / union_area


# 获取不同的bbox
def get_different_bboxes(bboxes1, bboxes2, iou_threshold=0.5):
    '''
    获取两个bbox列表中不同的bbox
    Args:
        bboxes1:
        bboxes2:
        iou_threshold:

    Returns:

    '''
    different_bboxes = []

    # 检查bboxes1中与bboxes2不同的bbox
    for bbox1 in bboxes1:
        is_different = True
        for bbox2 in bboxes2:
            if bbox1[0] != bbox2[0]:  # 检查类别是否相同
                continue
            if calculate_iou(bbox1[1:], bbox2[1:]) > iou_threshold:
                is_different = False
                break
        if is_different:
            different_bboxes.append(bbox1)

    # 检查bboxes2中与bboxes1不同的bbox
    for bbox2 in bboxes2:
        is_different = True
        for bbox1 in bboxes1:
            if bbox1[0] != bbox2[0]:  # 检查类别是否相同
                continue
            if calculate_iou(bbox1[1:], bbox2[1:]) > iou_threshold:
                is_different = False
                break
        if is_different:
            different_bboxes.append(bbox2)

    return different_bboxes


# 合并图片
def merge_images(image1, image2):
    '''
    合并两张图片
    Args:
        image1:
        image2:

    Returns:

    '''
    return cv2.hconcat([image1, image2])


# 保存图片
def save_image(image, save_path):
    '''
    保存图片
    Args:
        image:
        save_path:

    Returns:

    '''
    try:
        cv2.imwrite(save_path, image)
    except Exception as e:
        print(f"Error saving image to {save_path}, error: {e}")

def main(image_path, txt_path1, txt_path2, save_path, label_names):
    '''
    主函数
    Args:
        image_path:
        txt_path1:
        txt_path2:
        save_path:
        label_names:

    Returns:

    '''
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return
    img_height, img_width = image.shape[:2]
    bboxes1 = read_txt(txt_path1, img_width, img_height)
    bboxes2 = read_txt(txt_path2, img_width, img_height)
    image1 = draw_bboxes(image, bboxes1, label_names, (0, 0, 255))
    image2 = draw_bboxes(image, bboxes2, label_names, (0, 255, 0))
    different_bboxes = get_different_bboxes(bboxes1, bboxes2)
    image3 = draw_bboxes(image, different_bboxes, label_names, (255, 0, 0))
    merged_image = merge_images(image1, image2)
    merged_image = merge_images(merged_image, image3)
    save_image(merged_image, save_path)

def batch_process(image_folder, txt_folder1, txt_folder2, save_folder, label_names):
    '''
    批量处理图片
    Args:
        image_folder:
        txt_folder1:
        txt_folder2:
        save_folder:
        label_names:

    Returns:

    '''
    # 检查保存文件夹是否存在，如果不存在则创建
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    # 遍历图片文件夹
    # for image_name in os.listdir(image_folder):
    image_names = [image_name for image_name in os.listdir(image_folder) if
                   image_name.endswith(('.jpg', '.png', '.jpeg'))]
    for image_name in tqdm(image_names, desc="Processing images"):
        if not image_name.endswith(('.jpg', '.png', '.jpeg')):
            continue
        # 构建文件路径
        image_path = os.path.join(image_folder, image_name)
        txt_path1 = os.path.join(txt_folder1,image_name.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt'))
        txt_path2 = os.path.join(txt_folder2,image_name.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt'))
        save_path = os.path.join(save_folder, image_name)
        # 处理图片
        main(image_path, txt_path1, txt_path2, save_path, label_names)

if __name__ == '__main__':
    data_root = '/svap_storage/gatilin/data/hejing_pro/fixed_data/potential_miss_240509_6637done/ped_car_datasets/nomotor_bike_3cls_label_datasets'
    txt_folder1 = '/svap_storage/gatilin/datasets/ped_car_datasets/nomotor_bike_3cls_label_datasets/labels/train'

    image_folder = data_root + '/images/train'
    txt_folder2 = data_root + '/labels/train/'
    save_folder = data_root + '/check/'
    label_names = ['nomotor', 'bike', 'person', 'other']

    batch_process(image_folder, txt_folder1, txt_folder2, save_folder, label_names)
