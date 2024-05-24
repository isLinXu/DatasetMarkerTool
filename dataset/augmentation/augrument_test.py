import albumentations as A
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取原始图片
original_image = cv2.imread('/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/images/train2017/000000000009.jpg')

# 像素级变换
transform_Pixel = A.Compose([
    # A.CLAHE(p=1),  # 直方图均衡
    # A.ChannelDropout(p=1),  # 随机丢弃通道
    # A.ChannelShuffle(p=1),  # 随机排列通道
    A.ColorJitter(p=1),  # 随机改变图像的亮度、对比度、饱和度、色调
])

# 空间级变换
transform_Spatial = A.Compose([
    # A.RandomCrop(width=256, height=256),
    A.HorizontalFlip(p=1),
    A.RandomBrightnessContrast(brightness_limit=0.5, contrast_limit=0.5, p=1),  # 与像素级变换结合使用
    # A.SafeRotate(limit=60, p=1),
    # A.Rotate(limit=45, p=1),
    # A.Affine(p=1),
    # A.GridDistortion(p=1),

])

# 进行增强变化
transformed = transform_Spatial(image=original_image)

# 获得增强后的图片
transformed_image = transformed["image"]
transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

plt.subplot(1, 2, 1), plt.title("original image"), plt.axis('off')
plt.imshow(original_image)
plt.subplot(1, 2, 2), plt.title("transformed image"), plt.axis('off')
plt.imshow(transformed_image)

plt.show()
