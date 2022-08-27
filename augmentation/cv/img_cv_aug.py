# -*- coding: utf-8 -*-

"""
    ******不改变原始xml的一些数据增强方法 type 1-10*******
    把增强后的图像和xml一起放入新的文件夹
    rootpath:picture_xml原始路径
    savepath：picture_xml保存路径

    *******改变原始 xml的一些数据增强方法  type 11-15******
    修改图片的同时修改对应的xml
    file_path: 传入类别的信息txt，最好和生成labelmap的顺序一致
    rootpath: picture_xml原始路径
    savepath：picture_xml保存路径

    11:自定义裁剪，图像大小 w,h，例如 w=400,h=600
    12：自定义平移，平移比例 w,h [0-1] 例如w=0.1,h=0,2
    13：自定义缩放，调整图像大小 w,h,例如 w=400,h=600
    14：图像翻转
    15:图像任意旋转，传入旋转角度列表anglelist=[90,-90]
"""
import cv2
import random

from tqdm import tqdm

import math
import os
import shutil
import numpy as np
from PIL import Image, ImageStat
from skimage import exposure
import matplotlib.pyplot as plt
import tensorlayer as tl
from lxml.etree import Element, SubElement, tostring
import xml.etree.ElementTree as ET


def hisColor_Img(path):
    """
    对图像直方图均衡化
    :param path: 图片路径
    :return: 直方图均衡化后的图像
    """
    img = cv2.imread(path)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])  # equalizeHist(in,out)
    cv2.merge(channels, ycrcb)
    img_eq = cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR)
    return img_eq


def clahe_Img(path, ksize):
    """
    :param path: 图像路径
    :param ksize: 用于直方图均衡化的网格大小，默认为8
    :return: clahe之后的图像
    """
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(ksize, ksize))
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)
    image = cv2.merge([b, g, r])
    return image


def whiteBalance_Img(path):
    """
    对图像白平衡处理
    """
    img = cv2.imread(path)
    b, g, r = cv2.split(img)
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    Cr = 0.5 * r - 0.419 * g - 0.081 * b
    Cb = -0.169 * r - 0.331 * g + 0.5 * b
    Mr = np.mean(Cr)
    Mb = np.mean(Cb)
    Dr = np.var(Cr)
    Db = np.var(Cb)
    temp_arry = (np.abs(Cb - (Mb + Db * np.sign(Mb))) < 1.5 * Db) & (
            np.abs(Cr - (1.5 * Mr + Dr * np.sign(Mr))) < 1.5 * Dr)
    RL = Y * temp_arry
    # 选取候选白点数的最亮10%确定为最终白点，并选择其前10%中的最小亮度值
    L_list = list(np.reshape(RL, (RL.shape[0] * RL.shape[1],)).astype(np.int))
    hist_list = np.zeros(256)
    min_val = 0
    sum = 0
    for val in L_list:
        hist_list[val] += 1
    for l_val in range(255, 0, -1):
        sum += hist_list[l_val]
        if sum >= len(L_list) * 0.1:
            min_val = l_val
            break
    # 取最亮的前10%为最终的白点
    white_index = RL < min_val
    RL[white_index] = 0
    # 计算选取为白点的每个通道的增益
    b[white_index] = 0
    g[white_index] = 0
    r[white_index] = 0
    Y_max = np.max(RL)
    b_gain = Y_max / (np.sum(b) / np.sum(b > 0))
    g_gain = Y_max / (np.sum(g) / np.sum(g > 0))
    r_gain = Y_max / (np.sum(r) / np.sum(r > 0))
    b, g, r = cv2.split(img)
    b = b * b_gain
    g = g * g_gain
    r = r * r_gain
    # 溢出处理
    b[b > 255] = 255
    g[g > 255] = 255
    r[r > 255] = 255
    res_img = cv2.merge((b, g, r))
    return res_img


def bright_Img(path, ga, flag):
    """
    亮度增强 Tensorlayer
    :param ga: ga为gamma值，>1亮度变暗，<1亮度变亮
    :param flag:True: 亮度值为(1-ga,1+ga)
                False:亮度值为ga,默认为1
    :return: 亮度增强后的图像
    """
    image = tl.vis.read_image(path)
    tenl_img = tl.prepro.brightness(image, gamma=ga, is_random=flag)
    return tenl_img


def illumination_Img(path, ga, co, sa, flag):
    """
    亮度,饱和度，对比度增强 Tensorlayer
    :param ga: ga为gamma值，>1亮度变暗，<1亮度变亮
    :param co: 对比度值，1为原始值
    :param sa: 饱和度值，1为原始值
    :param flag:True: 亮度值为(1-ga,1+ga)，对比度(1-co,1+co)，饱和度(1-sa,1+sa)
                False:亮度值为ga,对比度co,饱和度sa
    :return:增强后的结果
    """
    image = tl.vis.read_image(path)
    tenl_img = tl.prepro.illumination(image, gamma=ga, contrast=co, saturation=sa, is_random=flag)
    return tenl_img


def create_mask(imgpath):
    image = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
    _, mask = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    return mask


def xiufu_Img(imgpath, maskpath):
    """
    去除图像上的高光部分
    """
    src_ = cv2.imread(imgpath)
    mask = cv2.imread(maskpath, cv2.IMREAD_GRAYSCALE)
    # 缩放因子(fx,fy)
    res_ = cv2.resize(src_, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_CUBIC)
    mask = cv2.resize(mask, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_CUBIC)
    dst = cv2.inpaint(res_, mask, 10, cv2.INPAINT_TELEA)
    return dst


def image_brightness(rgb_image):
    '''
    检测图像亮度(基于RMS)
    '''
    stat = ImageStat.Stat(rgb_image)
    r, g, b = stat.rms
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def calc_gamma(brightness):
    return brightness / 127.0


def image_gamma_transform(pil_im, gamma):
    image_arr = np.array(pil_im)
    image_arr2 = exposure.adjust_gamma(image_arr, gamma)
    if len(image_arr.shape) == 3:  # 格式为(height(rows), weight(colums), 3)
        r = Image.fromarray(np.uint8(image_arr[:, :, 0]))
        g = Image.fromarray(np.uint8(image_arr[:, :, 1]))
        b = Image.fromarray(np.uint8(image_arr[:, :, 2]))
        image = Image.merge("RGB", (r, g, b))
        return image
    elif len(image_arr.shape) == 2:  # 格式为(height(rows), weight(colums))
        return Image.fromarray(np.uint8(image_arr))


def autobright_Img(rootpath, savepath):
    """
    自适应亮度增强
    """
    list = os.listdir(rootpath)
    for i in range(0, len(list)):
        path = os.path.join(rootpath, list[i])
        if os.path.isfile(path):
            if list[i].endswith("jpg") or list[i].endswith("JPG") or list[i].endswith("png") or list[i].endswith("PNG"):
                print("adjust_bright running....")
                print(list[i])
                im = Image.open(path)
                brightness = image_brightness(im)
                newimage = np.array(image_gamma_transform(im, calc_gamma(brightness)))
                newname = "adjust_bright" + list[i][:-4]
                saveflie = os.path.join(savepath, newname + ".jpg")
                plt.imsave(saveflie, newimage)
                shutil.copyfile(os.path.join(rootpath, list[i][:-4] + ".xml"),
                                os.path.join(savepath, newname + ".xml"))


def probability_random_event(rate, event):
    """随机变量的概率函数"""
    #
    # 参数rate为list<int>
    # 返回概率事件的下标索引
    start = 0
    index = 0
    randnum = random.randint(1, sum(rate))

    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return event[index]


def erase_Img(root_path, save_path):
    """
    随机遮挡
    """
    for file in os.listdir(root_path):
        file_name, extension = os.path.splitext(file)
        if extension == '.xml':
            print("erase running....")
            print(file_name + ".jpg")
            xml_path = os.path.join(root_path, file)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            image_path = os.path.join(root_path, file_name + '.jpg')
            image = cv2.imread(image_path)
            for obj in root.findall('object'):
                # 文件夹图像遮挡的比例，参数可修改
                is_erase = probability_random_event([7, 3], [True, False])
                if is_erase:
                    # boundingbox遮挡的方向，参数可修改
                    erase_orientation = probability_random_event([6, 2, 1, 1],
                                                                 ['down', 'up', 'left', 'right'])
                    # 遮挡方块的大小，参数可修改
                    erase_scope = random.uniform(0.1, 0.3)
                    xml_box = obj.find('bndbox')
                    _xmin = int(xml_box.find('xmin').text)
                    _xmax = int(xml_box.find('xmax').text)
                    _ymin = int(xml_box.find('ymin').text)
                    _ymax = int(xml_box.find('ymax').text)
                    box_width = _xmax - _xmin
                    box_height = _ymax - _ymin
                    new_xmin, new_xmax, new_ymin, new_ymax = _xmin, _xmax, _ymin, _ymax
                    if erase_orientation == 'down':
                        new_ymax = int(_ymax - box_height * erase_scope)
                        image[new_ymax:_ymax, new_xmin:new_xmax, :] = 255
                    if erase_orientation == 'up':
                        new_ymin = int(_ymin + box_height * erase_scope)
                        image[_ymin:new_ymin, new_xmin:new_xmax, :] = 255
                    if erase_orientation == 'left':
                        new_xmin = int(_xmin + box_width * erase_scope)
                        image[new_ymin:new_ymax, _xmin:new_xmin, :] = 255
                    if erase_orientation == 'right':
                        new_xmax = int(_xmax - box_width * erase_scope)
                        image[new_ymin:new_ymax, new_xmax:_xmax, :] = 255
                    cv2.imwrite(os.path.join(save_path, "earse_" + file_name + '.jpg'), image)
                    xml_box.find('xmin').text = str(new_xmin)
                    xml_box.find('ymin').text = str(new_ymin)
                    xml_box.find('xmax').text = str(new_xmax)
                    xml_box.find('ymax').text = str(new_ymax)
                    tree.write(os.path.join(save_path, "earse_" + file_name + '.xml'))


def blur_Img(rootpath, savepath, ksize, new_rate):
    """
    随机模糊图像
    """
    img_list = []
    for imgfiles in os.listdir(rootpath):
        if (imgfiles.endswith("jpg") or imgfiles.endswith("JPG")):
            img_list.append(imgfiles)
    filenumber = len(img_list)
    rate = new_rate  # 自定义抽取文件夹中图片的比例，参数可修改
    picknumber = int(filenumber * rate)
    sample = random.sample(img_list, picknumber)
    for name in sample:
        print("blur running....")
        print(name)
        namepath = os.path.join(rootpath, name)
        ori_img = cv2.imread(namepath)
        size = random.choice(ksize)  # 设置高斯核的大小，参数可修改，size>9，小于9图像没有变化
        kernel_size = (size, size)
        image = cv2.GaussianBlur(ori_img, ksize=kernel_size, sigmaX=0, sigmaY=0)
        cv2.imwrite(os.path.join(savepath, "blur_" + name), image)
        shutil.copyfile(os.path.join(rootpath, name.split(".")[0] + ".xml"),
                        os.path.join(savepath, "blur_" + name.split(".")[0] + ".xml"))


def compress_Img(infile_path, outfile_path, pic_size):
    """
    压缩图像
    不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    """
    count = 0
    for infile in os.listdir(infile_path):
        if infile.endswith(".jpg") or infile.endswith(".GPG") or \
                infile.endswith(".jpeg") or infile.endswith(".GPEG"):
            print("compress_ running....")
            print(infile)
            filename, extend_name = os.path.splitext(infile)
            img_path = os.path.join(infile_path, infile)
            imgsaved_path = os.path.join(outfile_path, "compress_" + infile)
            img = cv2.imread(img_path, 1)
            # 获取文件大小:KB
            img_size = os.path.getsize(img_path) / 1024
            if img_size > pic_size:
                cv2.imwrite(imgsaved_path, img, [cv2.IMWRITE_JPEG_QUALITY, 30])
                shutil.copyfile(os.path.join(infile_path, filename + ".xml"),
                                os.path.join(outfile_path, "compress_" + filename + ".xml"))
            else:
                shutil.copyfile(img_path, imgsaved_path)
                shutil.copyfile(os.path.join(infile_path, filename + ".xml"),
                                os.path.join(outfile_path, "compress_" + filename + ".xml"))


#######改变原始 xml的一些数据增强方法  type 11-15############
def rotate_image(src, angle, scale=1):
    """
    :param src: 图像的地址
    :param angle: 旋转角度
    :param scale: 旋转范围
    :return: 旋转后的图像
    """
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    dst = cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
    return dst


def rotate_xml(src, xmin, ymin, xmax, ymax, angle, scale=1):
    """
    旋转xml
    """
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)
    # 获取旋转后图像的长和宽
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)

    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))

    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    point1 = np.dot(rot_mat, np.array([xmin, ymin, 1]))
    point2 = np.dot(rot_mat, np.array([xmax, ymin, 1]))
    point3 = np.dot(rot_mat, np.array([xmax, ymax, 1]))
    point4 = np.dot(rot_mat, np.array([xmin, ymax, 1]))
    concat = np.vstack((point1, point2, point3, point4))
    concat = concat.astype(np.int32)
    rx, ry, rw, rh = cv2.boundingRect(concat)
    return rx, ry, rx + rw, ry + rh


def get_classdict(file_path):
    """
    得到所有类别的字典,总类别
    :param file_path: 总类别的文本文件
    :return: 所有类别的列表，字典
    """
    classes = []
    classes_dict = {}
    for line in open(file_path):
        classes.append(line.strip("\n"))
    for i in range(len(classes)):
        classes_dict[classes[i]] = i + 1
    return classes, classes_dict


def trans_img(img, img_xml, classes_dict):
    """
    把数据转换为 ann_list的格式,ann_list=[类别，位置信息【list】]
    :param img: img
    :param img_xml: img_xml
    :param classes_dict: 总类别字典
    :return: class_list:xml中的类别,ann_list=[位置信息【list】
    """
    ann_list = []
    class_list = []
    tree = ET.parse(img_xml)
    root = tree.getroot()
    # 找到图像的w,h
    size = root.find('size')
    xml_width = int(size.find('width').text)
    xml_height = int(size.find('height').text)
    for obj in root.iter('object'):
        position = []
        # 类别信息
        xml_name = str(obj.find('name').text)
        if xml_name in classes_dict.keys():
            xml_class = classes_dict[xml_name]
            xml_box = obj.find('bndbox')
            _xmin = int(xml_box.find('xmin').text)
            _xmax = int(xml_box.find('xmax').text)
            _ymin = int(xml_box.find('ymin').text)
            _ymax = int(xml_box.find('ymax').text)
            c_x = ((_xmin + _xmax) / 2.0) / xml_width
            c_y = ((_ymin + _ymax) / 2.0) / xml_height
            o_w = (_xmax - _xmin) / xml_width
            o_h = (_ymax - _ymin) / xml_height
            position.append(c_x)
            position.append(c_y)
            position.append(o_w)
            position.append(o_h)
            class_list.append(xml_class)
            ann_list.append(position)
    return class_list, ann_list


#######type11-14:自定义裁剪，w,h>0，自定义平移，w,h:0-1，自定义缩放w,h >0，图像翻转 ###########
def handle_img(rootpath, savepath, classes, classes_dict, img, img_xml, w, h, type):
    """
    用tensorlayer 进行数据增强，包括裁剪，平移，缩放，翻转，得到增强后的图像和修改对应的xml,并保存在新的文件夹中
    :param rootpath: 图片+xml原始路径
    :param savepath: 图片+xml保存路径
    :param classes: 总类别
    :param classes_dict: 总类别词典
    :param img: 图像
    :param img_xml: img_xml
    :param w: 1：裁剪的尺寸w 2：平移比例 w 3：缩放的尺寸w
    :param h: 1：裁剪的尺寸h 2：平移比例 h 3：缩放的尺寸h
    :param type: 不同的数据增强方法。type=1:自定义裁剪，w,h>0 2：自定义平移，w,h:0-1 3：自定义缩放w,h >0  4：图像翻转
    :return: 直接保存数据增强后的图像+xml
    """
    global img_newxml, clas, coords
    anns = []
    # 得到总类别
    # sku包含的类别，归一化后得到坐标信息 ,is_random可以修改，默认裁剪中间
    img1 = os.path.join(rootpath, img)
    img1_xml = os.path.join(rootpath, img_xml)
    cla, ann = trans_img(img1, img1_xml, classes_dict)
    image = tl.vis.read_image(img1)
    ##随机裁剪图片######
    if type == 11:
        im_crop, clas, coords = tl.prepro.obj_box_crop(image, cla,
                                                       ann, wrg=w, hrg=h, is_rescale=True, is_center=True,
                                                       is_random=False)
        tl.vis.save_image(im_crop, os.path.join(savepath, "crop_" + img))
        image = im_crop.copy()
    ######位移#########
    if type == 12:
        im_shfit, clas, coords = tl.prepro.obj_box_shift(image, cla,
                                                         ann, wrg=w, hrg=h,
                                                         is_rescale=True, is_center=True, is_random=True)
        tl.vis.save_image(im_shfit, os.path.join(savepath, "shift_" + img))
        image = im_shfit.copy()
    #######调整图片大小 #####
    if type == 13:
        clas = cla
        im_resize, coords = tl.prepro.obj_box_imresize(image, coords=ann, size=[w, h], is_rescale=True)
        tl.vis.save_image(im_resize, os.path.join(savepath, "resize_" + img))
        image = im_resize.copy()
    #########图像翻转###########
    if type == 14:
        clas = cla
        im_flip, coords = tl.prepro.obj_box_horizontal_flip(image, coords=ann, is_rescale=True, is_center=True,
                                                            is_random=False)
        tl.vis.save_image(im_flip, os.path.join(savepath, "flip_" + img))
        image = im_flip.copy()
    imh, imw = image.shape[0:2]
    # clas类别信息 anns新的坐标信息，im_crop裁剪的图片
    for i in range(len(coords)):
        pos = []
        x, y, x2, y2 = tl.prepro.obj_box_coord_centroid_to_upleft_butright(coords[i])
        x, y, x2, y2 = tl.prepro.obj_box_coord_scale_to_pixelunit([x, y, x2, y2], (imh, imw))
        pos.append(x), pos.append(y), pos.append(x2), pos.append(y2)
        anns.append(pos)
    ###新建xml###########
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = '1'
    node_filename = SubElement(node_root, 'filename')
    if type == 11:
        node_filename.text = "crop_" + img
    if type == 12:
        node_filename.text = "shift_" + img
    if type == 13:
        node_filename.text = "resize_" + img
    if type == 14:
        node_filename.text = "filp_" + img
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(imw)
    node_height = SubElement(node_size, 'height')
    node_height.text = str(imh)
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in range(len(clas)):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = str(classes[clas[i] - 1])
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(anns[i][0])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(anns[i][1])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(anns[i][2])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(anns[i][3])
    xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
    if type == 11:
        img_newxml = os.path.join(savepath, "crop_" + img_xml)
    if type == 12:
        img_newxml = os.path.join(savepath, "shift_" + img_xml)
    if type == 13:
        img_newxml = os.path.join(savepath, "resize_" + img_xml)
    if type == 14:
        img_newxml = os.path.join(savepath, "flip_" + img_xml)
    file_object = open(img_newxml, 'wb')
    file_object.write(xml)
    file_object.close()


def route_pic_xml(rootpath, routepath, anglelist, rate):
    """
    ########type=5:旋转图像###################
    旋转图像和修改对应的xml,并保存在新的文件夹中
    :param rootpath: 原始路径
    :param routepath: 旋转后的路径
    :param anglelist: 旋转角度列表
    :param rate: 旋转图像的比例
    """
    for angle in anglelist:
        pathDir = []
        for i in os.listdir(rootpath):
            if i.endswith("jpg") or i.endswith("JPG"):
                pathDir.append(i)
        new_rate = rate  # 自定义抽取图片的比例
        picknumber = int(len(pathDir) * new_rate)
        print(picknumber)
        sample = random.sample(pathDir, picknumber)
        for name in sample:
            a, b = os.path.splitext(name)  # 分离出文件名a
            img = cv2.imread(os.path.join(rootpath, a + '.jpg'))
            rotated_img = rotate_image(img, angle)
            cv2.imwrite(os.path.join(routepath, str(angle) + "d"'_' + a + '.jpg'), rotated_img)
            print(a + ".jpg")
            tree = ET.parse(os.path.join(rootpath, a + '.xml'))
            root = tree.getroot()
            for box in root.iter('bndbox'):
                xmin = float(box.find('xmin').text)
                ymin = float(box.find('ymin').text)
                xmax = float(box.find('xmax').text)
                ymax = float(box.find('ymax').text)
                x, y, x1, y1 = rotate_xml(img, xmin, ymin, xmax, ymax, angle)
                box.find('xmin').text = str(x)
                box.find('ymin').text = str(y)
                box.find('xmax').text = str(x1)
                box.find('ymax').text = str(y1)
            tree.write(routepath + "/" + str(angle) + "d" + '_' + a + '.xml')
            print(a + ".xml")


if __name__ == '__main__':
    ###根据type值选择不同的数据增强的方法
    # 1.直方图均衡化
    # 2.clahe自适应对比度直方图均衡化
    # 3.白平衡
    # 4.亮度增强
    # 5.亮度，饱和度，对比度增强
    # 6.去除图像上的高光部分#####
    # 7.自适应亮度增强
    # 8.随机遮挡
    # 9.图像高斯模糊
    # 10.压缩图像#####
    # 11:自定义裁剪，图像大小 w,h，例如 w=400,height=600#####
    # 12：自定义平移，平移比例 w,h [0-1] 例如w=0.10,h=0,2#####
    # 13：自定义缩放，调整图像大小 w,h,例如 w=400,h=600#####
    # 14：图像翻转#####
    # 15:图像任意旋转，传入旋转角度列表anglelist=[90,-90]#####
    type = 3
    rootpath = r"/home/linxu/Desktop/广西恒信项目/现场图像-中铝智能巡检项目/现场图像"
    savepath = r"/home/linxu/Desktop/广西恒信项目/现场图像-中铝智能巡检项目/增强图像3"
    # type 6 去除高光需要给mask蒙版的保存地址
    masksavepath = r"/home/linxu/Desktop/广西恒信项目/现场图像-中铝智能巡检项目/WCP-data/mask"
    # type 11-15 需要传入 file_path:传入类别的信息txt，最好和生成labelmap的顺序一致
    file_path = r"/home/linxu/Desktop/广西恒信项目/现场图像-中铝智能巡检项目/wcp.txt"

    # 1.直方图均衡化 2.clahe自适应对比度直方图均衡化 3.白平衡 4.亮度增强 5.亮度，饱和度，对比度增强 6.去除图像上的高光部分
    if type in range(1, 7):
        imgfiles = os.listdir(rootpath)
        for i in tqdm(range(0, len(imgfiles))):
            path = os.path.join(rootpath, imgfiles[i])
            print(imgfiles[i])
            if os.path.isfile(path):
                if (imgfiles[i].endswith("jpg") or imgfiles[i].endswith("JPG")):
                    # 直方图均衡化
                    if type == 1:
                        print("hiscolor running....")
                        enhance_img = hisColor_Img(path)
                        newname = 'hiscolor_' + imgfiles[i].split(".")[0]
                        cv2.imwrite(os.path.join(savepath, newname + ".jpg"), enhance_img)
                    # clahe自适应对比度直方图均衡化
                    if type == 2:
                        print("clahe running....")
                        # 设置clahe直方图均衡化的网格大小
                        ksize = 8
                        enhance_img = clahe_Img(path, ksize)
                        newname = 'clahe_' + imgfiles[i].split(".")[0]
                        cv2.imwrite(os.path.join(savepath, newname + ".jpg"), enhance_img)
                    # 白平衡
                    if type == 3:
                        print("whiteBalance running....")
                        enhance_img = whiteBalance_Img(path)
                        newname = 'whiteBalance_' + imgfiles[i].split(".")[0]
                        cv2.imwrite(os.path.join(savepath, newname + ".jpg"), enhance_img)
                    # 亮度增强
                    if type == 4:
                        # 亮度值，可改变，>1亮度变暗，<1亮度变亮
                        # flag:True: 亮度值为(1-ga,1+ga) False:亮度值为ga,默认为1
                        print("bright running....")
                        ga = 0.8
                        flag = False
                        enhance_img = bright_Img(path, ga, flag)
                        newname = 'bright_' + imgfiles[i].split(".")[0]
                        tl.vis.save_image(enhance_img, os.path.join(savepath, newname + ".jpg"))
                    # 亮度，对比度，饱和度增强
                    if type == 5:
                        # ga: ga为亮度值，>1亮度变暗，<1亮度变亮
                        # co: 对比度值，1为原始值
                        # sa: 饱和度值，1为原始值
                        # flag: True: 亮度值为(1 - ga, 1 + ga)，对比度(1 - co, 1 + co)，饱和度(1 - sa, 1 + sa)
                        # False: 亮度值为ga, 对比度co, 饱和度sa
                        ga = 1
                        co = 0.9
                        sa = 1
                        flag = False
                        print("illumination running....")
                        enhance_img = illumination_Img(path, ga, co, sa, flag)
                        newname = 'illumination_' + imgfiles[i].split(".")[0]
                        tl.vis.save_image(enhance_img, os.path.join(savepath, newname + ".jpg"))
                    # 去除高光
                    if type == 6:
                        print("xiufu running....")
                        maskpath = os.path.join(masksavepath, "mask_" + imgfiles[i])
                        cv2.imwrite(maskpath, create_mask(path))
                        enhance_img = xiufu_Img(path, maskpath)
                        newname = 'xiufu_' + imgfiles[i].split(".")[0]
                        cv2.imwrite(os.path.join(savepath, newname + ".jpg"), enhance_img)

                    # shutil.copyfile(os.path.join(rootpath, imgfiles[i].split(".")[0] + ".xml"),
                    #                 os.path.join(savepath, newname + ".xml"))
    # 亮度自适应调节
    if type == 7:
        autobright_Img(rootpath, savepath)
    # 随机遮挡
    if type == 8:
        erase_Img(rootpath, savepath)
    # 高斯模糊
    if type == 9:
        # 设置高斯模糊核，越大越模糊
        ksize = (9, 11, 13, 17)
        # 设置模糊比例
        rate = 0.5
        blur_Img(rootpath, savepath, ksize, rate)
    # 压缩图像
    if type == 10:
        # 设置压缩图像的阈值，例如 pic_size=500，大于500的才压缩
        pic_size = 500
        compress_Img(rootpath, savepath, pic_size)
    # 自定义裁剪 or 自定义平移 or自定义缩放 or 图像翻转

    if type in range(11, 15):
        # 在type=1 or type=3 时，w,h尺寸大小，例如 w=600,h=800
        # 在type=2时，w,h为平移的比例，例如w=0.1,h=0.2
        # w =800
        # h =1280
        w = 0.1
        h = 0.2
        classes, classes_dict = get_classdict(file_path)
        list = os.listdir(rootpath)
        for i in range(0, len(list)):
            path = os.path.join(rootpath, list[i])
            if os.path.isfile(path):
                if (list[i].endswith("jpg") or list[i].endswith("JPG")):
                    img = list[i]
                    img_xml = list[i].split(".")[0] + ".xml"
                    im = Image.open(path)
                    print(img)
                    if im.size[0] > w and im.size[1] > h:
                        handle_img(rootpath, savepath, classes, classes_dict, img, img_xml, w, h, type)
    # 随机旋转
    if type == 15:
        # 旋转角度列表，旋转比例 例如 anglelist = [90, -90]
        anglelist = [90, ]
        rate = 0.5
        route_pic_xml(rootpath, savepath, anglelist, rate)
