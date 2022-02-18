#-*- coding:utf-8 -*-
import os, glob
import cv2
from scipy.io import loadmat
from collections import defaultdict
import numpy as np
from lxml import etree, objectify

def vbb_anno2dict(vbb_file, cam_id):
    filename = os.path.splitext(os.path.basename(vbb_file))[0]
    annos = defaultdict(dict)
    vbb = loadmat(vbb_file)
    # object info in each frame: id, pos, occlusion, lock, posv
    objLists = vbb['A'][0][0][1][0]
    objLbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]     #可查看所有类别
    print(objLbl)
    # person index
    person_index_list = np.where(np.array(objLbl) == "person")[0]   #只选取类别为‘person’的xml
    for frame_id, obj in enumerate(objLists):
        if len(obj) > 0:
            frame_name = str(cam_id) + "_" + str(filename) + "_" + str(frame_id).zfill(6) + ".jpg"
            annos[frame_name] = defaultdict(list)
            annos[frame_name]["id"] = frame_name
            annos[frame_name]["label"] = "person"
            for id, pos, occl in zip(obj['id'][0], obj['pos'][0], obj['occl'][0]):
                id = int(id[0][0]) - 1  # for matlab start from 1 not 0
                if not id in person_index_list:  # only use bbox whose label is person
                    continue
                pos = pos[0].tolist()
                occl = int(occl[0][0])
                annos[frame_name]["occlusion"].append(occl)
                annos[frame_name]["bbox"].append(pos)
            if not annos[frame_name]["bbox"]:
                del annos[frame_name]
    print(annos)
    return annos


def seq2img(annos, seq_file, outdir, cam_id):
    cap = cv2.VideoCapture(seq_file)
    index = 1
    # captured frame list
    v_id = os.path.splitext(os.path.basename(seq_file))[0]
    cap_frames_index = np.sort([int(os.path.splitext(id)[0].split("_")[2]) for id in annos.keys()])
    while True:
        ret, frame = cap.read()
        print(ret)
        if ret:
            if not index in cap_frames_index:
                index += 1
                continue
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            outname = os.path.join(outdir, str(cam_id)+"_"+v_id+"_"+str(index).zfill(6)+".jpg")
            print("Current frame: ", v_id, str(index))
            cv2.imwrite(outname, frame)
            height, width, _ = frame.shape
        else:
            break
        index += 1
    img_size = (width, height)
    return img_size


def instance2xml_base(anno, bbox_type='xyxy'):
    """bbox_type: xyxy (xmin, ymin, xmax, ymax); xywh (xmin, ymin, width, height)"""
    assert bbox_type in ['xyxy', 'xywh']
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('VOC2014_instance/person'),
        E.filename(anno['id']),
        E.source(
            E.database('Caltech pedestrian'),
            E.annotation('Caltech pedestrian'),
            E.image('Caltech pedestrian'),
            E.url('None')
        ),
        E.size(
            E.width(640),
            E.height(480),
            E.depth(3)
        ),
        E.segmented(0),
    )
    for index, bbox in enumerate(anno['bbox']):
        bbox = [float(x) for x in bbox]
        if bbox_type == 'xyxy':
            xmin, ymin, w, h = bbox
            xmax = xmin+w
            ymax = ymin+h
        else:
            xmin, ymin, xmax, ymax = bbox
        E = objectify.ElementMaker(annotate=False)
        anno_tree.append(
            E.object(
            E.name(anno['label']),
            E.bndbox(
                E.xmin(xmin),
                E.ymin(ymin),
                E.xmax(xmax),
                E.ymax(ymax)
            ),
            E.difficult(0),
            E.occlusion(anno["occlusion"][index])
            )
        )
    return anno_tree


def parse_anno_file(vbb_inputdir, seq_inputdir, vbb_outputdir, seq_outputdir):
    # annotation sub-directories in hda annotation input directory
    assert os.path.exists(vbb_inputdir)
    sub_dirs = os.listdir(vbb_inputdir)     #sub_dirs为每一个子目录
    for sub_dir in sub_dirs:
        print("Parsing annotations of camera: ", sub_dir)
        cam_id = sub_dir
        vbb_files = glob.glob(os.path.join(vbb_inputdir, sub_dir, "*.vbb")) #vbb_files在列表中并不是按数字顺序排列的
        for vbb_file in vbb_files:
            annos = vbb_anno2dict(vbb_file, cam_id)
            if annos:
                # vbb_outdir = os.path.join(vbb_outputdir, "annotations", sub_dir, "bbox")
                vbb_outdir = os.path.join(vbb_outputdir, "Annotations")
                # extract frames from seq
                # seq_file = os.path.join(seq_inputdir, sub_dir, os.path.splitext(os.path.basename(vbb_file))[0]+".seq")
                # seq_outdir = os.path.join(seq_outputdir, sub_dir, "frame")
                if not os.path.exists(vbb_outdir):
                    os.makedirs(vbb_outdir)
                # if not os.path.exists(seq_outdir):
                #     os.makedirs(seq_outdir)
                #img_size = seq2img(annos, seq_file, seq_outdir, cam_id)
                for filename, anno in sorted(annos.items(), key=lambda x: x[0]):
                    if "bbox" in anno:
                        anno_tree = instance2xml_base(anno)
                        a0,a1,a2 = (os.path.splitext(filename)[0]).split('_')
                        a2 = str(int(a2)).zfill(6)
                        a = a0+ "_" +a1+ "_"+a2
                        outfile = os.path.join(vbb_outdir, a +".xml")
                        print("Generating annotation xml file of picture: ", filename)
                        etree.ElementTree(anno_tree).write(outfile, pretty_print=True)


def visualize_bbox(xml_file, img_file):
    import cv2
    tree = etree.parse(xml_file)
    # load image
    image = cv2.imread(img_file)
    # get bbox
    for bbox in tree.xpath('//bndbox'):
        coord = []
        for corner in bbox.getchildren():
            coord.append(int(float(corner.text)))
        print(coord)
        # draw rectangle
        # coord = [int(x) for x in coord]
        cv2.rectangle(image, (coord[0], coord[1]), (coord[2], coord[3]), (0, 0, 255), 2)
    # visualize image
    cv2.imshow("test", image)
    cv2.waitKey(1)

def vis_single():
    xml_file = "./data/annotations/set00/bbox/set00_V000_258.xml"
    img_file =  "./data/images/set00/images/set00_V000_258.jpg"
    visualize_bbox(xml_file, img_file)

def vis_batch():
    for xml_file in sorted(glob.glob('{}/*.xml'.format("./data/VOCdevkit/VOC2007/Annotations/"))):
        filename = os.path.splitext(os.path.split(xml_file)[1])[0]
        img_file = "./data/images/set01/images/" + str(filename) + ".jpg"
        print(img_file)
        visualize_bbox(xml_file, img_file)

def main():
    seq_inputdir = "./data/images/set00"
    vbb_inputdir = "./data/annotations"
    seq_outputdir = "./data/images/"
    vbb_outputdir = "./data/VOCdevkit/VOC2007/"
    if not os.path.exists(vbb_outputdir):
        os.makedirs(vbb_outputdir)
    parse_anno_file(vbb_inputdir, seq_inputdir, vbb_outputdir, seq_outputdir)



if __name__ == "__main__":
    main()