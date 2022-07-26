from lxml import etree
from PIL import Image
import csv
import os

# (NOTICE #1)
# If you're OS is Mac, there's a case when '.DS_Store' file is  automatically created.
# In that case, you have to remove '.DS_Store' file through the terminal.
# Ref : http://leechoong.com/posts/2018/ds_store/
# (NOTICE #2)
# Change this path variable
# YOUR_IMG_FOLDER_PATH
img_path = "/home/hxzh02/图片/coco128/images/train2017/"

# path of save xml file
save_path = '/home/hxzh02/图片/coco128/xml/'  # keep it blank

# txt_folder is txt file root that using darknet rectbox
# YOUR_TXT_FOLDER_PATH
txt_folder = '/home/hxzh02/图片/coco128/labels/train2017/'

# (NOTICE #3)
# Change this labels
labels = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']


def yolotxt_to_xml(img_path, save_path, txt_folder,labels):
    fw = os.listdir(img_path)
    for line in fw:
        root = etree.Element("annotation")

        # try debug to check your path
        img_style = img_path.split('/')[-1]
        img_name = line
        image_info = img_path + "/" + line
        img_txt_root = txt_folder + "/" + line[:-4]
        # print(img_txt_root)
        txt = ".txt"

        txt_path = img_txt_root + txt
        # print(txt_path)
        txt_file = csvread(txt_path)
        ######################################

        # read the image  information
        img_size = Image.open(image_info).size

        img_width = img_size[0]
        img_height = img_size[1]
        img_depth = Image.open(image_info).layers
        ######################################

        folder = etree.Element("folder")
        folder.text = "%s" % (img_style)

        filename = etree.Element("filename")
        filename.text = "%s" % (img_name)

        path = etree.Element("path")
        path.text = "%s" % (img_path)

        source = etree.Element("source")
        ##################source - element##################
        source_database = etree.SubElement(source, "database")
        source_database.text = "Unknown"
        ####################################################

        size = etree.Element("size")
        ####################size - element##################
        image_width = etree.SubElement(size, "width")
        image_width.text = "%d" % (img_width)

        image_height = etree.SubElement(size, "height")
        image_height.text = "%d" % (img_height)

        image_depth = etree.SubElement(size, "depth")
        image_depth.text = "%d" % (img_depth)
        ####################################################

        segmented = etree.Element("segmented")
        segmented.text = "0"

        root.append(folder)
        root.append(filename)
        root.append(path)
        root.append(source)
        root.append(size)
        root.append(segmented)

        for ii in range(len(txt_file)):
            label = convert_label(txt_file[ii][0])
            x_min_rect, x_max_rect, y_min_rect, y_max_rect = extract_coor(
                txt_file[ii], img_width, img_height)

            object = etree.Element("object")
            ####################object - element##################
            name = etree.SubElement(object, "name")
            name.text = "%s" % (label)

            pose = etree.SubElement(object, "pose")
            pose.text = "Unspecified"

            truncated = etree.SubElement(object, "truncated")
            truncated.text = "0"

            difficult = etree.SubElement(object, "difficult")
            difficult.text = "0"

            bndbox = etree.SubElement(object, "bndbox")
            #####sub_sub########
            xmin = etree.SubElement(bndbox, "xmin")
            xmin.text = "%d" % (x_min_rect)
            ymin = etree.SubElement(bndbox, "ymin")
            ymin.text = "%d" % (y_min_rect)
            xmax = etree.SubElement(bndbox, "xmax")
            xmax.text = "%d" % (x_max_rect)
            ymax = etree.SubElement(bndbox, "ymax")
            ymax.text = "%d" % (y_max_rect)
            #####sub_sub########

            root.append(object)
            ####################################################

        file_output = etree.tostring(root, pretty_print=True, encoding='UTF-8')
        # print(file_output.decode('utf-8'))
        ff = open(save_path + '%s.xml' % (img_name[:-4]), 'w', encoding="utf-8")
        ff.write(file_output.decode('utf-8'))





def csvread(fn):
    with open(fn, 'r') as csvfile:
        list_arr = []
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            list_arr.append(row)
    return list_arr


def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if txt_file == str(i):
            label = labels[i]
            return label

    return label


# core code = convert the yolo txt file to the x_min,x_max...


def extract_coor(txt_file, img_width, img_height):
    x_rect_mid = float(txt_file[1])
    y_rect_mid = float(txt_file[2])
    width_rect = float(txt_file[3])
    height_rect = float(txt_file[4])

    x_min_rect = ((2 * x_rect_mid * img_width) - (width_rect * img_width)) / 2
    x_max_rect = ((2 * x_rect_mid * img_width) + (width_rect * img_width)) / 2
    y_min_rect = ((2 * y_rect_mid * img_height) -
                  (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) +
                  (height_rect * img_height)) / 2

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect



