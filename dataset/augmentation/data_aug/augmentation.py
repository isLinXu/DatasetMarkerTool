from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import numpy as np
import random

def auto_contrast(image):
    """
    自动对比度调整。
    :param image: 输入图像 (PIL Image)
    :return: 对比度调整后的图像 (PIL Image)
    """
    return ImageOps.autocontrast(image)

# 调用示例
image = Image.open('example.jpg')
image = auto_contrast(image)
image.show()

def bbox_cutout(image, bboxes, cutout_size):
    """
    在边界框内随机选择一个位置进行cutout操作。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param cutout_size: cutout方块的大小
    :return: 进行cutout操作后的图像 (PIL Image)
    """
    draw = ImageDraw.Draw(image)
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        cutout_x = random.randint(x1, x2 - cutout_size)
        cutout_y = random.randint(y1, y2 - cutout_size)
        draw.rectangle([cutout_x, cutout_y, cutout_x + cutout_size, cutout_y + cutout_size], fill=(0, 0, 0))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = bbox_cutout(image, bboxes, 30)
image.show()

def brightness(image, factor):
    """
    调整图像亮度。
    :param image: 输入图像 (PIL Image)
    :param factor: 亮度增强因子，0.0会产生黑色图像，1.0保持原始图像
    :return: 亮度调整后的图像 (PIL Image)
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# 调用示例
image = Image.open('example.jpg')
image = brightness(image, 1.5)
image.show()

def color(image, factor):
    """
    调整图像颜色。
    :param image: 输入图像 (PIL Image)
    :param factor: 颜色增强因子，0.0会产生黑白图像，1.0保持原始图像
    :return: 颜色调整后的图像 (PIL Image)
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

# 调用示例
image = Image.open('example.jpg')
image = color(image, 1.5)
image.show()

def contrast(image, factor):
    """
    调整图像对比度。
    :param image: 输入图像 (PIL Image)
    :param factor: 对比度增强因子，0.0会产生纯灰色图像，1.0保持原始图像
    :return: 对比度调整后的图像 (PIL Image)
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# 调用示例
image = Image.open('example.jpg')
image = contrast(image, 1.5)
image.show()

def cutout(image, cutout_size):
    """
    在图像上随机选择一个位置进行cutout操作。
    :param image: 输入图像 (PIL Image)
    :param cutout_size: cutout方块的大小
    :return: 进行cutout操作后的图像 (PIL Image)
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    cutout_x = random.randint(0, width - cutout_size)
    cutout_y = random.randint(0, height - cutout_size)
    draw.rectangle([cutout_x, cutout_y, cutout_x + cutout_size, cutout_y + cutout_size], fill=(0, 0, 0))
    return image

# 调用示例
image = Image.open('example.jpg')
image = cutout(image, 30)
image.show()

def cutout_only_bboxes(image, bboxes, cutout_size):
    """
    在边界框内进行cutout操作。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param cutout_size: cutout方块的大小
    :return: 进行cutout操作后的图像 (PIL Image)
    """
    return bbox_cutout(image, bboxes, cutout_size)

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = cutout_only_bboxes(image, bboxes, 30)
image.show()

def equalize(image):
    """
    对图像进行直方图均衡化。
    :param image: 输入图像 (PIL Image)
    :return: 直方图均衡化后的图像 (PIL Image)
    """
    return ImageOps.equalize(image)

# 调用示例
image = Image.open('example.jpg')
image = equalize(image)
image.show()

def equalize_only_bboxes(image, bboxes):
    """
    在边界框内进行直方图均衡化。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :return: 进行直方图均衡化操作后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = ImageOps.equalize(sub_image)
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = equalize_only_bboxes(image, bboxes)
image.show()

def flip(image):
    """
    左右翻转图像。
    :param image: 输入图像 (PIL Image)
    :return: 翻转后的图像 (PIL Image)
    """
    return ImageOps.mirror(image)

# 调用示例
image = Image.open('example.jpg')
image = flip(image)
image.show()

def flip_only_bboxes(image, bboxes):
    """
    只左右翻转边界框。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :return: 翻转后的图像 (PIL Image)
    """
    width, _ = image.size
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        new_x1 = width - x2
        new_x2 = width - x1
        bbox[:] = [new_x1, y1, new_x2, y2]
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = flip_only_bboxes(image, bboxes)
image.show()

def posterize(image, bits):
    """
    减少图像的颜色位数。
    :param image: 输入图像 (PIL Image)
    :param bits: 保留的颜色位数，范围[0, 8]
    :return: 颜色位数减少后的图像 (PIL Image)
    """
    return ImageOps.posterize(image, bits)

# 调用示例
image = Image.open('example.jpg')
image = posterize(image, 4)
image.show()

def rotate_with_bboxes(image, angle):
    """
    旋转图像。
    :param image: 输入图像 (PIL Image)
    :param angle: 旋转角度
    :return: 旋转后的图像 (PIL Image)
    """
    return image.rotate(angle, expand=True)

# 调用示例
image = Image.open('example.jpg')
image = rotate_with_bboxes(image, 45)
image.show()

def sharpness(image, factor):
    """
    调整图像锐度。
    :param image: 输入图像 (PIL Image)
    :param factor: 锐度增强因子，0.0会产生模糊图像，1.0保持原始图像，2.0会产生锐化过的图像
    :return: 锐度调整后的图像 (PIL Image)
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

# 调用示例
image = Image.open('example.jpg')
image = sharpness(image, 2.0)
image.show()

def shear_x_bbox(image, factor):
    """
    在x方向上对图像进行剪切变换。
    :param image: 输入图像 (PIL Image)
    :param factor: 剪切因子
    :return: 剪切变换后的图像 (PIL Image)
    """
    return image.transform(image.size, Image.AFFINE, (1, factor, 0, 0, 1, 0))

# 调用示例
image = Image.open('example.jpg')
image = shear_x_bbox(image, 0.2)
image.show()

def shear_y_bbox(image, factor):
    """
    在y方向上对图像进行剪切变换。
    :param image: 输入图像 (PIL Image)
    :param factor: 剪切因子
    :return: 剪切变换后的图像 (PIL Image)
    """
    return image.transform(image.size, Image.AFFINE, (1, 0, 0, factor, 1, 0))

# 调用示例
image = Image.open('example.jpg')
image = shear_y_bbox(image, 0.2)
image.show()

def solarize(image, threshold):
    """
    对图像进行solarize操作。
    :param image: 输入图像 (PIL Image)
    :param threshold: 阈值
    :return: 进行solarize操作后的图像 (PIL Image)
    """
    return ImageOps.solarize(image, threshold)

# 调用示例
image = Image.open('example.jpg')
image = solarize(image, 128)
image.show()

def solarize_add(image, add_value, threshold):
    """
    对图像进行solarize_add操作。
    :param image: 输入图像 (PIL Image)
    :param add_value: 增加的像素值
    :param threshold: 阈值
    :return: 进行solarize_add操作后的图像 (PIL Image)
    """
    np_image = np.array(image)
    np_image = np.where(np_image < threshold, np_image + add_value, np_image)
    np_image = np.clip(np_image, 0, 255)
    return Image.fromarray(np_image.astype('uint8'))

# 调用示例
image = Image.open('example.jpg')
image = solarize_add(image, 50, 128)
image.show()

def solarize_only_bboxes(image, bboxes, threshold):
    """
    在边界框内进行solarize操作。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param threshold: 阈值
    :return: 进行solarize操作后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = ImageOps.solarize(sub_image, threshold)
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = solarize_only_bboxes(image, bboxes, 128)
image.show()

def shear_x_only_bboxes(image, bboxes, factor):
    """
    在x方向上只对边界框进行剪切变换。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param factor: 剪切因子
    :return: 剪切变换后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = sub_image.transform(sub_image.size, Image.AFFINE, (1, factor, 0, 0, 1, 0))
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = shear_x_only_bboxes(image, bboxes, 0.2)
image.show()

def shear_y_only_bboxes(image, bboxes, factor):
    """
    在y方向上只对边界框进行剪切变换。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param factor: 剪切因子
    :return: 剪切变换后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = sub_image.transform(sub_image.size, Image.AFFINE, (1, 0, 0, factor, 1, 0))
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = shear_y_only_bboxes(image, bboxes, 0.2)
image.show()

def translate_x_bbox(image, offset):
    """
    在x方向上对图像进行平移。
    :param image: 输入图像 (PIL Image)
    :param offset: 平移的像素数
    :return: 平移后的图像 (PIL Image)
    """
    return image.transform(image.size, Image.AFFINE, (1, 0, offset, 0, 1, 0))

# 调用示例
image = Image.open('example.jpg')
image = translate_x_bbox(image, 50)
image.show()

def translate_y_bbox(image, offset):
    """
    在y方向上对图像进行平移。
    :param image: 输入图像 (PIL Image)
    :param offset: 平移的像素数
    :return: 平移后的图像 (PIL Image)
    """
    return image.transform(image.size, Image.AFFINE, (1, 0, 0, 0, 1, offset))

# 调用示例
image = Image.open('example.jpg')
image = translate_y_bbox(image, 50)
image.show()

def translate_x_only_bboxes(image, bboxes, offset):
    """
    在x方向上只对边界框进行平移。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param offset: 平移的像素数
    :return: 平移后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = sub_image.transform(sub_image.size, Image.AFFINE, (1, 0, offset, 0, 1, 0))
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = translate_x_only_bboxes(image, bboxes, 50)
image.show()

def translate_y_only_bboxes(image, bboxes, offset):
    """
    在y方向上只对边界框进行平移。
    :param image: 输入图像 (PIL Image)
    :param bboxes: 边界框列表，每个边界框为[x1, y1, x2, y2]
    :param offset: 平移的像素数
    :return: 平移后的图像 (PIL Image)
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        sub_image = image.crop((x1, y1, x2, y2))
        sub_image = sub_image.transform(sub_image.size, Image.AFFINE, (1, 0, 0, 0, 1, offset))
        image.paste(sub_image, (x1, y1, x2, y2))
    return image

# 调用示例
image = Image.open('example.jpg')
bboxes = [[50, 50, 150, 150]]
image = translate_y_only_bboxes(image, bboxes, 50)
image.show()