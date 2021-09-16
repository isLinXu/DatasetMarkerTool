# -*- coding: utf-8 -*-

import cv2
import numpy as np

if __name__ == '__main__':

    # 读取模板图像
    # image = cv2.imread("reference.png")
    # image_gary = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)  # 转换成灰度图
    # print(image.shape)
    #
    # # 初始化一个与原图像等同的矩阵
    # temp = np.zeros((255, 386))
    # temp = temp.astype(np.uint8)
    #
    # # 查找图像中的矩阵
    # ret, thresh = cv2.threshold(image_gary, 250, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(thresh, 2, 1)
    # cnt = contours[0]
    # x, y, w, h = cv2.boundingRect(cnt)
    # img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示水印图片
    image2 = cv2.imread("watermark.png")
    roi = image2[y:y + h, x:x + w, 0:3]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY)
    ret, roi = cv2.threshold(roi, 80, 100, cv2.THRESH_BINARY)
    roi = cv2.morphologyEx(roi, cv2.MORPH_ELLIPSE, (5, 5))

    # 将水印图片赋值给初始化的矩阵图片
    roi2 = temp[y:y + h, x:x + w]
    roi3 = cv2.add(roi, roi2)
    temp[y:y + h, x:x + w] = roi3

    dst = cv2.inpaint(image2, temp, 30, cv2.INPAINT_NS)  # 使用INPAINT_TELEA算法进行修复
    cv2.imshow('TELEA', dst)
    cv2.waitKey(0)
