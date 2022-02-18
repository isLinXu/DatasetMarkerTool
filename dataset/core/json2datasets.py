import argparse
import base64
import json
import os
import os.path as osp
import cv2

import imgviz
import PIL.Image
from imgviz import label

from labelme.logger import logger
from labelme import utils
from numpy import save


def convert_single_img(i, json_file, save_dir):
    """
    将单个json文件转换为标签图像

    Args:
        i ([type]): [description]
        json_file (str): json文件
        out ([type]): [description]
    """
    # parser = argparse.ArgumentParser()
    # parser.add_argument("json_file")
    # parser.add_argument("-o", "--out", default=None)
    # args = parser.parse_args()

    # json_file = json_file

    if save_dir is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    if not osp.exists(save_dir):
        os.mkdir(save_dir)
    train_dir = osp.join(save_dir, 'train')
    if not osp.exists(train_dir):
        os.mkdir(train_dir)
    label_dir = osp.join(save_dir, 'label')
    if not osp.exists(label_dir):
        os.mkdir(label_dir)

    data = json.load(open(json_file))
    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)

    label_name_to_value = {"_background_": 0}
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl, _ = utils.shapes_to_label(img.shape, data["shapes"],
                                   label_name_to_value)

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name

    # lbl_viz = imgviz.label2rgb(label=lbl,
    #                            img=imgviz.asgray(img),
    #                            label_names=label_names,
    #                            loc="rb")

    PIL.Image.fromarray(img).save(osp.join(train_dir, f"{i}.png"))
    utils.lblsave(osp.join(label_dir, f"{i}.png"), lbl)
    # PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "label_viz.png"))
    label_name_file = osp.join(save_dir, "label_names.txt")
    if not os.path.isfile(label_name_file):
        with open(label_name_file, "w") as f:
            for lbl_name in label_names:
                f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(save_dir))


def get_json_file(base_dir='C:\\Users\\Ety\\Desktop\\labelme\\dataset'):
    json_file_list = []
    class_paths = [osp.join(base_dir, c) for c in os.listdir(base_dir)]
    for p in class_paths:
        if os.path.isdir(p):
            data = [
                os.path.join(p, f) for f in os.listdir(p)
                if f.endswith('.json')
            ]
            json_file_list.extend(data)
        else:
            if p.endswith('.json'):
                json_file_list.append(p)
    print(json_file_list)
    print(len(json_file_list))
    return json_file_list


def convert_img(path='./output/label'):
    imlist = [os.path.join(path, f) for f in os.listdir(path)]
    for im in imlist:
        gray = cv2.imread(im, 0)
        _, binary = cv2.threshold(gray, 0, 255,
                                  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # cv2.imshow('binary', binary)
        # cv2.waitKey()
        cv2.imwrite(im, binary)


def main():
    json_file_list = get_json_file()
    for i, f in json_file_list:
        convert_single_img(i, f, '.output')
    convert_img()


if __name__ == "__main__":
    main()
