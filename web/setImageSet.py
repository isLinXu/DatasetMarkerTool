#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###########
Usage:
python getImages.py image_path (annotation_path)

'''
import os
# import cPickle
import pickle
import xml.etree.ElementTree as ET


def voc2012():
    pass


def coco():
    pass


def dianwang():
    pass


def voc2007(annotationPath, cache_file):
    """TODO: Docstring for voc2007.
    :returns: TODO

    """
    if not os.path.exists(cache_file):
        print('parse annotation file...')
        files = os.listdir(annotationPath)
        files = sorted(files)
        annotation = []
        for f in files:
            assert (f.endswith('xml'))
            tree = ET.parse(os.path.join(annotationPath, f))
            width = tree.find('size').find('width').text
            height = tree.find('size').find('height').text
            boxes = []
            objs = tree.findall('object')
            for ix, obj in enumerate(objs):
                objName = obj.find('name').text
                bbox = obj.find('bndbox')
                x1 = float(bbox.find('xmin').text) - 1
                y1 = float(bbox.find('ymin').text) - 1
                x2 = float(bbox.find('xmax').text) - 1
                y2 = float(bbox.find('ymax').text) - 1
                boxes.append([objName, width, height, x1, y1, x2, y2])
            annotation.append(boxes)

        with open(cache_file, 'wb') as fid:
            pickle.dump(annotation, fid, pickle.HIGHEST_PROTOCOL)
        print('wrote voc2007 annotation to {}'.format(cache_file))


def editJS(content):
    assert len(content) == 2
    with open('web/main.js', 'r') as fid:
        lines = fid.readlines()
    with open('web/main.js', 'w') as fid:
        for l in lines:
            if 'var filepath' in l:
                fid.write(content[0] + '\n')
            elif 'var loadImage' in l:
                fid.write(content[1] + '\n')
            else:
                fid.write(l)


def getImages(filepath):
    # filepath = argv[1]
    if not filepath.endswith('/'):
        filepath += '/'
    files = os.listdir(filepath)
    files = sorted(files)
    loadImage = "{\"Date\":["
    for f in files:
        if f.endswith('jpg') or f.endswith('JPG'):
            loadImage += "{"
            loadImage += "\"src\":"
            loadImage += "\"{}\"".format(f)
            loadImage += "},"
    loadImage += "]}"

    contents = []
    contents.append("var filepath=\"{}\"".format(filepath))
    contents.append("var loadImage={}".format(loadImage))
    return contents


def main():
    # import sys
    # if len(sys.argv) < 2:
    #     print(__doc__)
    #     return
    # editJS(getImages(sys.argv))
    filepath = '/home/linxu/Desktop/visualize_imageset/林旭'
    editJS(getImages(filepath))
    # if len(sys.argv) == 4:
    annotationPath = '/home/linxu/Desktop/visualize_imageset/林旭xml2'
    cache_file = 'indexss'
    voc2007(annotationPath, cache_file)


if __name__ == "__main__":
    main()
