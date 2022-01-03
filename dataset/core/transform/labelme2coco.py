import os
import argparse
import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
from labelme import utils
import numpy as np
import glob
import PIL.Image

REQUIRE_MASK = False

class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path='./new.json'):
        '''
        :param labelme_json: the list of all labelme json file paths
        :param save_json_path: the path to save new json
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[]
        self.annotations=[]
        # self.data_coco = {}
        self.label=[]
        self.annID=1
        self.height=0
        self.width=0
        self.require_mask = REQUIRE_MASK
        self.save_json()

    def data_transfer(self):
        for num,json_file in enumerate(self.labelme_json):
            if not json_file == self.save_json_path:
                with open(json_file,'r') as fp:
                    data = json.load(fp)
                    self.images.append(self.image(data,num))
                    for shapes in data['shapes']:
                        print("label is ")
                        print(shapes['label'])
                        label=shapes['label']
    #                    if label[1] not in self.label:
                        if label not in self.label:
                            print("find new category: ")
                            self.categories.append(self.categorie(label))
                            print(self.categories)
                            # self.label.append(label[1])
                            self.label.append(label)
                        points=shapes['points']
                        self.annotations.append(self.annotation(points,label,num))
                        self.annID+=1

    def image(self,data,num):
        image={}
        img = utils.img_b64_to_arr(data['imageData'])
        # img=io.imread(data['imagePath'])
        # img = cv2.imread(data['imagePath'], 0)
        height, width = img.shape[:2]
        img = None
        image['height']=height
        image['width'] = width
        image['id']=num+1
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label):
        categorie={}
        categorie['supercategory'] = label
        categorie['id']=len(self.label)+1
        categorie['name'] = label
#        categorie['name'] = label[1]
        return categorie

    def annotation(self,points,label,num):
        annotation={}
        print(points)
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[1][0]
        y2 = points[1][1]
        contour = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]) #points = [[x1, y1], [x2, y2]] for rectangle
        contour = contour.astype(int)
        area = cv2.contourArea(contour)
        print("contour is ", contour, " area = ", area)
        annotation['segmentation']= [list(np.asarray([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]).flatten())]
        #[list(np.asarray(contour).flatten())]
        annotation['iscrowd'] = 0
        annotation['area'] = area
        annotation['image_id'] = num+1

        if self.require_mask:
            annotation['bbox'] = list(map(float,self.getbbox(points)))
        else:
            x1 = points[0][0]
            y1 = points[0][1]
            width = points[1][0] - x1
            height = points[1][1] - y1
            annotation['bbox']= list(np.asarray([x1, y1, width, height]).flatten())

        annotation['category_id'] = self.getcatid(label)
        annotation['id'] = self.annID
        return annotation

    def getcatid(self,label):
        for categorie in self.categories:
            if label == categorie['name']:
                return categorie['id']
        return -1

    def getbbox(self,points):
        polygons = points
        mask = self.polygons_to_mask([self.height,self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]

    def polygons_to_mask(self,img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco={}
        data_coco['images']=self.images
        data_coco['categories']=self.categories
        data_coco['annotations']=self.annotations
        return data_coco

    def save_json(self):
        print("save coco json")
        self.data_transfer()
        self.data_coco = self.data2coco()

        print(self.save_json_path)
        os.makedirs(
            os.path.dirname(os.path.abspath(self.save_json_path)), exist_ok=True
        )
        json.dump(self.data_coco, open(self.save_json_path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="labelme annotation to coco data json file."
    )
    parser.add_argument(
        "--labelme_images",
        help="Directory to labelme images and annotation json files.",
        type=str,
        default='pigimage',
    )
    parser.add_argument(
        "--output", help="Output json file path.", default="trainval.json"
    )
    args = parser.parse_args()
    # if args.labelme_images is None:
    #     args.labelme_images = '/home/hxzh02/WORK/yolact/data/data_tower/json/'
    #     args.output = '/home/hxzh02/WORK/yolact/data/data_tower/json_output'
    args.labelme_images = '/media/hxzh02/SB@home/hxzh/Dataset/PPLTA航拍输电线路数据集/data_original_size/'
    args.output = '/media/hxzh02/SB@home/hxzh/Dataset/PPLTA航拍输电线路数据集/data_original_size/instance_train2017.json'

    labelme_json = glob.glob(os.path.join(args.labelme_images, "*.json"))
    labelme2coco(labelme_json, args.output)

