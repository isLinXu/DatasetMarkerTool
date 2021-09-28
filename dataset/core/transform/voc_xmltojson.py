import xml.etree.ElementTree as ET
import os
import json

#转换的格式不是coco格式

lut={}
lut["i1"] =0
lut["i10"] =0
lut["i11"] =0
lut["i12"] =0
lut["i13"] =0
lut["i14"] =0
lut["i15"] =0
lut["i2"] =0
lut["i3"] =0
lut["i4"] =0
lut["i5"] =0
lut["il100"] =0
lut["il110"] =0
lut["il50"] =0
lut["il60"] =0
lut["il70"] =0
lut["il80"] =0
lut["il90"] =0
lut["io"] =0
lut["ip"] =0
lut["p1"] =1
lut["p10"] =1
lut["p11"] =1
lut["p12"] =1
lut["p13"] =1
lut["p14"] =1
lut["p15"] =1
lut["p16"] =1
lut["p17"] =1
lut["p18"] =1
lut["p19"] =1
lut["p2"] =1
lut["p20"] =1
lut["p21"] =1
lut["p22"] =1
lut["p23"] =1
lut["p24"] =1
lut["p25"] =1
lut["p26"] =1
lut["p27"] =1
lut["p28"] =1
lut["p3"] =1
lut["p4"] =1
lut["p5"] =1
lut["p6"] =1
lut["p7"] =1
lut["p8"] =1
lut["p9"] =1
lut["pa10"] =1
lut["pa12"] =1
lut["pa13"] =1
lut["pa14"] =1
lut["pa8"] =1
lut["pb"] =1
lut["pc"] =1
lut["pg"] =1
lut["ph1.5"] =1
lut["ph2"] =1
lut["ph2.1"] =1
lut["ph2.2"] =1
lut["ph2.4"] =1
lut["ph2.5"] =1
lut["ph2.8"] =1
lut["ph2.9"] =1
lut["ph3"] =1
lut["ph3.2"] =1
lut["ph3.5"] =1
lut["ph3.8"] =1
lut["ph4"] =1
lut["ph4.2"] =1
lut["ph4.3"] =1
lut["ph4.5"] =1
lut["ph4.8"] =1
lut["ph5"] =1
lut["ph5.3"] =1
lut["ph5.5"] =1
lut["pl10"] =1
lut["pl100"] =1
lut["pl110"] =1
lut["pl120"] =1
lut["pl15"] =1
lut["pl20"] =1
lut["pl25"] =1
lut["pl30"] =1
lut["pl35"] =1
lut["pl40"] =1
lut["pl5"] =1
lut["pl50"] =1
lut["pl60"] =1
lut["pl65"] =1
lut["pl70"] =1
lut["pl80"] =1
lut["pl90"] =1
lut["pm10"] =1
lut["pm13"] =1
lut["pm15"] =1
lut["pm1.5"] =1
lut["pm2"] =1
lut["pm20"] =1
lut["pm25"] =1
lut["pm30"] =1
lut["pm35"] =1
lut["pm40"] =1
lut["pm46"] =1
lut["pm5"] =1
lut["pm50"] =1
lut["pm55"] =1
lut["pm8"] =1
lut["pn"] =1
lut["pne"] =1
lut["po"] =1
lut["pr10"] =1
lut["pr100"] =1
lut["pr20"] =1
lut["pr30"] =1
lut["pr40"] =1
lut["pr45"] =1
lut["pr50"] =1
lut["pr60"] =1
lut["pr70"] =1
lut["pr80"] =1
lut["ps"] =1
lut["pw2"] =1
lut["pw2.5"] =1
lut["pw3"] =1
lut["pw3.2"] =1
lut["pw3.5"] =1
lut["pw4"] =1
lut["pw4.2"] =1
lut["pw4.5"] =1
lut["w1"] =2
lut["w10"] =2
lut["w12"] =2
lut["w13"] =2
lut["w16"] =2
lut["w18"] =2
lut["w20"] =2
lut["w21"] =2
lut["w22"] =2
lut["w24"] =2
lut["w28"] =2
lut["w3"] =2
lut["w30"] =2
lut["w31"] =2
lut["w32"] =2
lut["w34"] =2
lut["w35"] =2
lut["w37"] =2
lut["w38"] =2
lut["w41"] =2
lut["w42"] =2
lut["w43"] =2
lut["w44"] =2
lut["w45"] =2
lut["w46"] =2
lut["w47"] =2
lut["w48"] =2
lut["w49"] =2
lut["w5"] =2
lut["w50"] =2
lut["w55"] =2
lut["w56"] =2
lut["w57"] =2
lut["w58"] =2
lut["w59"] =2
lut["w60"] =2
lut["w62"] =2
lut["w63"] =2
lut["w66"] =2
lut["w8"] =2
lut["wo"] =2
lut["i6"] =0
lut["i7"] =0
lut["i8"] =0
lut["i9"] =0
lut["ilx"] =0
lut["p29"] =1
lut["w29"] =2
lut["w33"] =2
lut["w36"] =2
lut["w39"] =2
lut["w4"] =2
lut["w40"] =2
lut["w51"] =2
lut["w52"] =2
lut["w53"] =2
lut["w54"] =2
lut["w6"] =2
lut["w61"] =2
lut["w64"] =2
lut["w65"] =2
lut["w67"] =2
lut["w7"] =2
lut["w9"] =2
lut["pax"] =1
lut["pd"] =1
lut["pe"] =1
lut["phx"] =1
lut["plx"] =1
lut["pmx"] =1
lut["pnl"] =1
lut["prx"] =1
lut["pwx"] =1
lut["w11"] =2
lut["w14"] =2
lut["w15"] =2
lut["w17"] =2
lut["w19"] =2
lut["w2"] =2
lut["w23"] =2
lut["w25"] =2
lut["w26"] =2
lut["w27"] =2
lut["pl0"] =1
lut["pl4"] =1
lut["pl3"] =1
lut["pm2.5"] =1
lut["ph4.4"] =1
lut["pn40"] =1
lut["ph3.3"] =1
lut["ph2.6"] =1

try:
    json_file = open('GTSRB_classes.json', 'r')
    class_dict = json.load(json_file)
except Exception as e:
    print(e)
    exit(-1)


coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()

category_item_id = 0
image_id = 20180000000
annotation_id = 0


def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item['supercategory'] = 'none'
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    coco['categories'].append(category_item)
    category_set[name] = category_item_id
    return category_item_id


def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    # image_id += 1
    image_id=file_name.split(".ppm")[0]
    image_item = dict()
    image_item['file_name'] = image_id
    image_item['width'] = size['width']
    image_item['height'] = size['height']
    image_item['id'] = image_id
    print("image_item",image_item)

    coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id


def addAnnoItem(object_name, image_id, category_id, bbox):
    global annotation_id
    annotation_item = dict()
    # annotation_item['segmentation'] = []
    # seg = []
    # # bbox[] is x,y,w,h
    # # left_top
    # seg.append(bbox[0])
    # seg.append(bbox[1])
    # # left_bottom
    # seg.append(bbox[0])
    # seg.append(bbox[1] + bbox[3])
    # # right_bottom
    # seg.append(bbox[0] + bbox[2])
    # seg.append(bbox[1] + bbox[3])
    # # right_top
    # seg.append(bbox[0] + bbox[2])
    # seg.append(bbox[1])
    #
    # annotation_item['segmentation'].append(seg)

    annotation_item['area'] = bbox[2] * bbox[3]
    annotation_item['iscrowd'] = 0
    annotation_item['image_id'] = image_id
    annotation_item['bbox'] = bbox
    annotation_item['category_id'] = category_id
    annotation_id += 1
    annotation_item['id'] = annotation_id
    annotation_item['ignore'] = 0
    coco['annotations'].append(annotation_item)
    with open("test_gt_TT100Kthree.txt","a") as read:
        read.write(str(image_id)+";"+str(bbox[0])+";"+str(bbox[1])+";"+str(bbox[2])+";"+str(bbox[3])+";"+str(category_id)+"\n")




def parseXmlFiles(xml_path):
    for f in os.listdir(xml_path):
        if not f.endswith('.xml'):
            continue

        bndbox = dict()
        size = dict()
        current_image_id = None
        current_category_id = None
        file_name = None
        size['width'] = None
        size['height'] = None
        size['depth'] = None

        xml_file = os.path.join(xml_path, f)
        print(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        # elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            current_parent = elem.tag
            current_sub = None
            object_name = None

            if elem.tag == 'folder':
                continue

            if elem.tag == 'filename':
                file_name = elem.text
                if file_name in category_set:
                    raise Exception('file_name duplicated')

            # add img item only after parse <size> tag
            elif current_image_id is None and file_name is not None and size['width'] is not None:
                if file_name not in image_set:
                    current_image_id = addImgItem(file_name, size)
                    print('add image with {} and {}'.format(file_name, size))
                else:
                    raise Exception('duplicated image: {}'.format(file_name))
                    # subelem is <width>, <height>, <depth>, <name>, <bndbox>
            for subelem in elem:
                bndbox['xmin'] = None
                bndbox['xmax'] = None
                bndbox['ymin'] = None
                bndbox['ymax'] = None

                current_sub = subelem.tag
                if current_parent == 'object' and subelem.tag == 'name':
                    object_name = subelem.text
                    if object_name in lut:
                        current_category_id = lut[object_name]
                        # prohibitory = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 16]
                        # danger = [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
                        # mandatory = [33, 34, 35, 36, 37, 38, 39, 40]
                        # other = [6, 12, 13, 14, 17, 32, 41, 42]
                        # if class_dict[object_name] in prohibitory:
                        #     current_category_id=1
                        # elif class_dict[object_name] in danger:
                        #     current_category_id=2
                        # elif class_dict[object_name] in mandatory:
                        #     current_category_id=3
                        # elif class_dict[object_name] in other:
                        #     current_category_id=4


                    # if object_name not in category_set:
                    #     print("not in #########################",object_name)
                    #     current_category_id = addCatItem(object_name)
                    # else:
                    #     if object_name  in lut:
                    #         # current_category_id = category_set[object_name]
                    #         current_category_id=lut[object_name]

                elif current_parent == 'size':
                    if size[subelem.tag] is not None:
                        raise Exception('xml structure broken at size tag.')
                    size[subelem.tag] = int(subelem.text)

                # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                for option in subelem:
                    if current_sub == 'bndbox':
                        if bndbox[option.tag] is not None:
                            raise Exception('xml structure corrupted at bndbox tag.')
                        bndbox[option.tag] = int(option.text)

                # only after parse the <object> tag
                if bndbox['xmin'] is not None:
                    if object_name is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_image_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_category_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    bbox = []
                    # x
                    bbox.append(bndbox['xmin'])
                    # y
                    bbox.append(bndbox['ymin'])

                    bbox.append(bndbox['xmax'])
                    bbox.append(bndbox['ymax'])
                    # # w
                    # bbox.append(bndbox['xmax'] - bndbox['xmin'])
                    # # h
                    # bbox.append(bndbox['ymax'] - bndbox['ymin'])
                    print('add annotation with {},{},{},{}'.format(object_name, current_image_id, current_category_id,
                                                                   bbox))
                    addAnnoItem(object_name, current_image_id, current_category_id, bbox)


if __name__ == '__main__':
    xml_path = '/home/dell/桌面/TT100K/VOC2007/Annotations'
    json_file = 'TT100K_instances.json'

    parseXmlFiles(xml_path)
    json.dump(coco, open(json_file, 'w'))
