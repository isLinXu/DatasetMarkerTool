import imageio
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
from tqdm import tqdm

ia.seed(42)


def generate_xml(save_path, img_info):
    doc = Document()
    DOCUMENT = doc.createElement('annotation')

    floder = doc.createElement('folder')
    floder_text = doc.createTextNode(img_info["folder"])
    floder.appendChild(floder_text)
    DOCUMENT.appendChild(floder)
    doc.appendChild(DOCUMENT)

    filename = doc.createElement('filename')
    filename_text = doc.createTextNode(img_info["filename"])  # filename:
    filename.appendChild(filename_text)
    DOCUMENT.appendChild(filename)
    doc.appendChild(DOCUMENT)

    path = doc.createElement('path')
    path_text = doc.createTextNode(img_info["img_path"])  # path:
    path.appendChild(path_text)
    DOCUMENT.appendChild(path)
    doc.appendChild(DOCUMENT)

    source = doc.createElement('source')
    database = doc.createElement('database')
    database_text = doc.createTextNode('Unknow')
    database.appendChild(database_text)
    source.appendChild(database)
    DOCUMENT.appendChild(source)
    doc.appendChild(DOCUMENT)

    size = doc.createElement('size')
    width = doc.createElement('width')
    width_text = doc.createTextNode(str(img_info["img_shape"][1]))
    width.appendChild(width_text)
    size.appendChild(width)

    height = doc.createElement('height')
    height_text = doc.createTextNode(str(img_info["img_shape"][0]))
    height.appendChild(height_text)
    size.appendChild(height)

    depth = doc.createElement('depth')
    depth_text = doc.createTextNode(str(img_info["img_shape"][2]))
    depth.appendChild(depth_text)
    size.appendChild(depth)

    DOCUMENT.appendChild(size)

    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    DOCUMENT.appendChild(segmented)
    doc.appendChild(DOCUMENT)

    objectes = img_info["object"]

    if len(objectes) == 0:
        return

    for obj in objectes:
        _object = doc.createElement('object')
        name = doc.createElement('name')
        name_text = doc.createTextNode(obj["category"])
        name.appendChild(name_text)
        _object.appendChild(name)

        pose = doc.createElement('pose')
        pose_text = doc.createTextNode('Unspecified')
        pose.appendChild(pose_text)
        _object.appendChild(pose)

        truncated = doc.createElement('truncated')
        truncated_text = doc.createTextNode('0')
        truncated.appendChild(truncated_text)
        _object.appendChild(truncated)

        truncated = doc.createElement('difficult')
        truncated_text = doc.createTextNode('0')
        truncated.appendChild(truncated_text)
        _object.appendChild(truncated)

        bndbox = doc.createElement('bndbox')
        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(str(int(obj["bbox"][0])))
        xmin.appendChild(xmin_text)
        bndbox.appendChild(xmin)

        ymin = doc.createElement('ymin')
        ymin_text = doc.createTextNode(str(int(obj["bbox"][1])))
        ymin.appendChild(ymin_text)
        bndbox.appendChild(ymin)

        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(str(int(obj["bbox"][2])))
        xmax.appendChild(xmax_text)
        bndbox.appendChild(xmax)

        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(str(int(obj["bbox"][3])))
        ymax.appendChild(ymax_text)
        bndbox.appendChild(ymax)
        _object.appendChild(bndbox)
        DOCUMENT.appendChild(_object)

    f = open(save_path, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t')
    f.close()


def parse_xml(xml_path):
    dict_info = {'cat': [], 'bboxes': [], 'box_wh': [], 'whd': []}
    tree = ET.parse(xml_path)
    root = tree.getroot()
    whd = root.find('size')
    whd = [int(whd.find('width').text), int(whd.find('height').text), int(whd.find('depth').text)]
    for obj in root.findall('object'):
        cat = str(obj.find('name').text)
        bbox = obj.find('bndbox')
        x1, y1, x2, y2 = [int(bbox.find('xmin').text),
                          int(bbox.find('ymin').text),
                          int(bbox.find('xmax').text),
                          int(bbox.find('ymax').text)]
        b_w = x2 - x1 + 1
        b_h = y2 - y1 + 1
        dict_info['cat'].append(cat)
        dict_info['bboxes'].append([x1, y1, x2, y2])
        dict_info['box_wh'].append([b_w, b_h])
        dict_info['whd'].append(whd)
    return dict_info


def get_bbox(xml):
    box_res = []
    tree = ET.parse(xml)
    root = tree.getroot()
    for obj in root.findall('object'):
        name = obj.find('name').text
        for box in obj.findall('bndbox'):
            xmin = int(float(box.find('xmin').text))
            ymin = int(float(box.find('ymin').text))
            xmax = int(float(box.find('xmax').text))
            ymax = int(float(box.find('ymax').text))
            box_res.append(BoundingBox(x1=xmin, y1=ymin, x2=xmax, y2=ymax, label=name))
    return box_res


def get_all_files(img_root):
    img_paths = []
    img_names = []
    for root, _, files in os.walk(img_root):
        if files is not None:
            for file in files:
                if file.endswith('xml'):
                    img_paths.append(os.path.join(root, file))
                    img_names.append(file)
    return img_paths, img_names


def get_all_files_list(all_path):
    xml_path_list = []
    xml_names_list = []
    img_paths_list = []
    img_names_list = []
    for root, _, files in os.walk(all_path):
        if files is not None:
            for file in files:
                if file.endswith('xml'):
                    xml_path = os.path.join(root, file)
                    print('xml_path', xml_path)
                    xml_path_list.append(xml_path)
                    xml_names_list.append(file)
                if file.endswith('jpg'):
                    img_path = os.path.join(root, file)
                    print('img_path', img_path)
                    img_paths_list.append(img_path)
                    img_names_list.append(file)
    return img_paths_list, img_names_list, xml_path_list, xml_names_list


if __name__ == '__main__':
    save_path = r'/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/img_aug/'
    save_img_path = r'/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/img_aug/' + 'JPEGImages'
    save_xml_path = r'/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/img_aug/' + 'Annotations'
    all_path = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007'
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_img_path, exist_ok=True)
    os.makedirs(save_xml_path, exist_ok=True)
    img_paths_list, img_names_list, xml_path_list, xml_names_list = get_all_files_list(all_path)

    for i in tqdm(range(0, len(xml_path_list))):
        xml_path = xml_path_list[i]
        jpg_path = img_paths_list[i]
        filename = img_names_list[i]
        print('jpg_path', jpg_path)
        if os.path.exists(jpg_path):
            box = get_bbox(xml_path)
            img = imageio.imread(jpg_path)
            bbs = BoundingBoxesOnImage(box, img.shape)
            image_before = bbs.draw_on_image(img, size=2)
            # 图像的transform方式
            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                # iaa.Affine(translate_px={"x": 50, "y": 60}, scale=(0.5, 0.7)),
                iaa.AdditiveGaussianNoise(scale=0.1 * 255),
                iaa.Rotate(rotate=(-10, 10))
            ], random_order=True)
            image_aug, bbs_aug = seq(image=img, bounding_boxes=bbs)
            bbs_aug_clip = bbs_aug.remove_out_of_image().clip_out_of_image()  # clip box out of img
            if len(bbs_aug_clip) > 0:
                parse_info = parse_xml(xml_path)
                img_info = {
                    'img_shape': parse_info['whd'][0],
                    'folder': os.path.split(xml_path)[0],
                    'filename': filename,
                    'img_path': jpg_path,
                    'object': [{'category': b.label, 'bbox': [b.x1, b.y1, b.x2, b.y2]} for b in
                               bbs_aug_clip.bounding_boxes]}
                generate_xml(os.path.join(save_xml_path, os.path.split(xml_path)[-1]), img_info)
                imageio.imwrite(os.path.join(save_img_path, filename), image_aug)
            else:
                print('bboxes are out of boundry, {}'.format(jpg_path))
