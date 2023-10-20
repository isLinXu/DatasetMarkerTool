from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import skimage.io as io
import matplotlib.pyplot as plt

classes_names = ["person", "bicycle", "car", "motorbike", "bus", "truck"]

headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
# """

tailstr = '''\
</annotation>
'''
#
def showimg(coco, dataset, img, classes, cls_id, show=True):
    global dataDir
    I = Image.open('%s/%s/%s/%s' % (dataDir, 'images', dataset, img['file_name']))
    # Get the annotated information by ID
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=cls_id, iscrowd=None)
    # print(annIds)
    anns = coco.loadAnns(annIds)
    # print(anns)
    # coco.showAnns(anns)
    objs = []
    for ann in anns:
        class_name = classes[ann['category_id']]
        if class_name in classes_names:
            print(class_name)
            if 'bbox' in ann:
                bbox = ann['bbox']
                xmin = int(bbox[0])
                ymin = int(bbox[1])
                xmax = int(bbox[2] + bbox[0])
                ymax = int(bbox[3] + bbox[1])
                obj = [class_name, xmin, ymin, xmax, ymax]
                objs.append(obj)
                draw = ImageDraw.Draw(I)
                draw.rectangle([xmin, ymin, xmax, ymax])
    if show:
        plt.figure()
        plt.axis('off')
        plt.imshow(I)
        plt.show()

    return objs

from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import cv2
from PIL import Image, ImageDraw


def extract_coco_class(data_dir, save_path, classes_names, datasets_list=['train2014']):
    img_dir = os.path.join(save_path, 'images/')
    anno_dir = os.path.join(save_path, 'Annotations/')

    def mkr(path):
        if os.path.exists(path):
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            os.mkdir(path)

    mkr(img_dir)
    mkr(anno_dir)

    def id2name(coco):
        classes = dict()
        for cls in coco.dataset['categories']:
            classes[cls['id']] = cls['name']
        return classes

    def write_xml(anno_path, head, objs, tail):
        with open(anno_path, "w") as f:
            f.write(head)
            for obj in objs:
                f.write(objstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
            f.write(tail)

    def save_annotations_and_imgs(coco, dataset, filename, objs):
        anno_path = os.path.join(anno_dir, filename[:-3] + 'xml')
        img_path = os.path.join(data_dir, dataset, filename)
        dst_imgpath = os.path.join(img_dir, filename)

        img = cv2.imread(img_path)
        shutil.copy(img_path, dst_imgpath)

        head = headstr % (filename, img.shape[1], img.shape[0], img.shape[2])
        tail = tailstr
        write_xml(anno_path, head, objs, tail)

    for dataset in datasets_list:
        ann_file = os.path.join(data_dir, 'annotations/instances_{}.json'.format(dataset))
        coco = COCO(ann_file)
        classes = id2name(coco)

        classes_ids = coco.getCatIds(catNms=classes_names)

        for cls in classes_names:
            cls_id = coco.getCatIds(catNms=[cls])
            img_ids = coco.getImgIds(catIds=cls_id)

            for imgId in tqdm(img_ids):
                img = coco.loadImgs(imgId)[0]
                filename = img['file_name']
                objs = showimg(coco, dataset, img, classes, classes_ids, show=False)
                save_annotations_and_imgs(coco, dataset, filename, objs)


# Example Usage:
dataDir = '/media/deepnorth/14b6945d-9936-41a8-aeac-505b96fc2be8/COCO/'
savePath = '/media/deepnorth/14b6945d-9936-41a8-aeac-505b96fc2be8/COCO_processed/'
classesNames = ['bicycle']
extract_coco_class(dataDir, savePath, classesNames)
