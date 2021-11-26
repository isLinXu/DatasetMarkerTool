
import Image

def read_image(image_path, filename):
    '''
    读取图片属性
    :param image_path:
    :param filename:
    :return:
    '''
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area = W * H
    im_info = [W, H, area]
    return im_info