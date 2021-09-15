
import os.path as osp
import xml.etree.ElementTree as ET

#import mmcv  #需在mmdet环境下！
import json

from glob import glob
from tqdm import tqdm
from PIL import Image

cls_classes = ['dog','cat','human']    #检测目标类别（不含background）
label_ids = {name: i + 1 for i, name in enumerate(cls_classes)}

def get_segmentation(points):
    return [points[0], points[1], points[2] + points[0], points[1],
             points[2] + points[0], points[3] + points[1], points[0], points[3] + points[1]]

def parse_xml(xml_path, img_id, anno_id):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    annotation = []
    for obj in root.findall('object'):
        try:
            name = obj.find('name').text       
            category_id = label_ids[name]
            bnd_box = obj.find('bndbox')   
            xmin = int(bnd_box.find('xmin').text)
            ymin = int(bnd_box.find('ymin').text)
            xmax = int(bnd_box.find('xmax').text)
            ymax = int(bnd_box.find('ymax').text)
            if xmin>=xmax or ymin>=ymax:
                continue
            w = xmax - xmin + 1
            h = ymax - ymin + 1
            area = w*h
            segmentation = get_segmentation([xmin, ymin, w, h])
            annotation.append({
                            "segmentation": segmentation,
                            "area": area,
                            "iscrowd": 0,
                            "image_id": img_id,
                            "bbox": [xmin, ymin, w, h],
                            "category_id": category_id,
                            "id": anno_id,
                            "ignore": 0})
            anno_id += 1
        except:
            continue
    return annotation, anno_id

def cvt_annotations(img_path, xml_path, out_file):
    images = []
    annotations = []
    img_id = 1
    anno_id = 1
    for img_path in tqdm(glob(img_path + '/*.jpg')):
        w, h = Image.open(img_path).size
        img_name = osp.basename(img_path)
        img = {"file_name": img_name, "height": int(h), "width": int(w), "id": img_id}
        images.append(img)

        xml_file_name = img_name.split('.')[0] + '.xml'
        xml_file_path = osp.join(xml_path, xml_file_name)
        annos, anno_id = parse_xml(xml_file_path, img_id, anno_id)
        annotations.extend(annos)
        img_id += 1

    categories = []
    for k,v in label_ids.items():
        categories.append({"name": k, "id": v})
    final_result = {"images": images, "annotations": annotations, "categories": categories} #COCO数据集格式
    #mmcv.dump(final_result, out_file) 需在mmdet环境下！
    with open(out_file, 'w') as f:
        json.dump(final_result, f, indent=4)
    return annotations


def main():
    xml_path = "/home1/huangqiangHD/dataset/train/xml/"   #XML文件位置
    img_path = "/home1/huangqiangHD/dataset/train/images/"#Image文件位置
    out_path = "/home1/huangqiangHD/dataset/train/train.json"#COCO文件位置
    print('processing {} ...'.format("xml format annotations"))
    cvt_annotations(img_path, xml_path, out_path)
    print('Done!')


if __name__ == '__main__':
    main()
