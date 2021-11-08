from multiprocessing import Pool
import cv2
import glob
import os.path as osp
import os
import numpy as np
from typing import Tuple

class YoloImageSplitTool(object):
    def __init__(self,
                 in_root:str,
                 out_root:str,
                 tile_overlap:Tuple[int, int],
                 tile_shape:Tuple[int, int],
                 num_process=8,
                 ):
        self.in_images_dir = osp.join(in_root, 'images/')
        self.in_labels_dir = osp.join(in_root, 'dotalabels/')
        self.out_images_dir = osp.join(out_root, 'images/')
        self.out_labels_dir = osp.join(out_root, 'dotalabels/')
        assert isinstance(tile_shape, tuple), f'argument "tile_shape" must be tuple but got {type(tile_shape)} instead!'
        assert isinstance(tile_overlap,
                          tuple), f'argument "tile_overlap" must be tuple but got {type(tile_overlap)} instead!'
        self.tile_overlap = tile_overlap
        self.tile_shape = tile_shape
        images = glob.glob(self.in_images_dir + '*.jpg')
        labels = glob.glob(self.in_labels_dir + '*.txt')
        image_ids = [*map(lambda x: osp.splitext(osp.split(x)[-1])[0], images)]
        label_ids = [*map(lambda x: osp.splitext(osp.split(x)[-1])[0], labels)]
        assert set(image_ids) == set(label_ids)
        self.image_ids = image_ids
        if not osp.isdir(out_root):
            os.makedirs(out_root)
        if not osp.isdir(self.out_images_dir):
            os.makedirs(self.out_images_dir)
        if not osp.isdir(self.out_labels_dir):
            os.makedirs(self.out_labels_dir)
        self.num_process = num_process

    def _parse_annotation_single(self, image_id):
        label_dir = osp.join(self.in_labels_dir, image_id + '.txt')
        with open(label_dir, 'r') as f:
            s = f.readlines()
        objects = []
        for si in s:
            bbox_info = si.split()
            assert len(bbox_info) == 9
            bbox = [*map(lambda x: int(x), bbox_info[:8])]
            center = sum(bbox[0::2]) / 4.0, sum(bbox[1::2]) / 4.0
            objects.append({'bbox': bbox,
                            'label': bbox_info[8],
                            'center': center})
        return  objects

    def _split_single(self, image_id):
        objs = self._parse_annotation_single(image_id)
        image_dir = osp.join(self.in_images_dir, image_id + '.png')
        # img = cv2.imread(image_dir)
        img = cv2.imdecode(np.fromfile(image_dir, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        h, w, _ = img.shape
        overlap_w, overlap_h = self.tile_overlap
        crop_w, crop_h = self.tile_shape
        h_step = crop_h - overlap_h if h > crop_h else h
        for h_off in range(0, h, h_step):
            if h_off + crop_h >= h:
                h_off = max(h - crop_h,0)

            w_step = crop_w - overlap_w if w > crop_w else w
            for w_off in range(0, w, w_step):
                if w_off + crop_w >= w:
                    w_off = max(w - crop_w,0)                
                objs_tile = []
                for obj in objs:
                    if w_off <= obj['center'][0] <= w_off + crop_w - 1:
                        if h_off <= obj['center'][1] <= h_off + crop_h - 1:
                            objs_tile.append(obj)
                if len(objs_tile) > 0:
                    img_tile = img[h_off:h_off + crop_h, w_off:w_off + crop_w, :]
                    save_image_dir = osp.join(self.out_images_dir, f'{image_id}_{w_off}_{h_off}.png')
                    save_label_dir = osp.join(self.out_labels_dir, f'{image_id}_{w_off}_{h_off}.txt')
                    # cv2.imwrite(save_image_dir, img_tile)
                    cv2.imencode(".png",img_tile)[1].tofile(save_image_dir)
                    label_tile = []
                    for obj in objs_tile:
                        px, py = obj["bbox"][0::2], obj["bbox"][1::2]
                        px = map(lambda x: str(x - w_off), px)
                        py = map(lambda x: str(x - h_off), py)
                        bbox_tile = sum([*zip(px, py)], ())
                        obj_s = f'{" ".join(bbox_tile)} {obj["label"]}\n'
                        label_tile.append(obj_s)
                    with open(save_label_dir, 'w') as f:
                        f.writelines(label_tile)

    def split(self):
        with Pool(self.num_process) as p:
            p.map(self._split_single, self.image_ids)


if __name__ == '__main__':
    dir="../test/"

    valsplit = YoloImageSplitTool(dir,
                                  dir+'/temp',
                                  tile_overlap=(150, 150),
                                  tile_shape=(600, 600))
    valsplit.split()
