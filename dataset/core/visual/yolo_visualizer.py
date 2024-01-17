import os
import streamlit as st
import cv2
from PIL import Image

# 设置页面标题
st.title("YOLO 数据集可视化")

# 选择图像文件夹
image_folder_path = st.text_input("输入图像文件夹路径:", value="")

# 选择标签文件夹
label_folder_path = st.text_input("输入标签文件夹路径:", value="")

if image_folder_path:
    image_files = os.listdir(image_folder_path)
    images = [file for file in image_files if file.endswith(".jpg") or file.endswith(".png")]

    # 选择图像文件
    image_file = st.selectbox("选择图像文件:", images)

    if image_file:
        # 显示图像
        image_path = os.path.join(image_folder_path, image_file)
        image = Image.open(image_path)
        st.image(image, caption="原始图像", use_column_width=True)

        if label_folder_path:
            label_files = os.listdir(label_folder_path)
            annotations = [file for file in label_files if file.endswith(".txt")]

            # 显示标注
            annotation_file = os.path.splitext(image_file)[0] + ".txt"
            if annotation_file in annotations:
                with open(os.path.join(label_folder_path, annotation_file), "r") as file:
                    content = file.read()
                    st.write("标注内容:")
                    st.write(content)

                    # 在图像上绘制边界框
                    image_cv = cv2.imread(image_path)
                    height, width, _ = image_cv.shape
                    with open(os.path.join(label_folder_path, annotation_file), "r") as file:
                        for line in file.readlines():
                            class_id, x, y, w, h = map(float, line.strip().split())
                            x_min = int((x - w / 2) * width)
                            x_max = int((x + w / 2) * width)
                            y_min = int((y - h / 2) * height)
                            y_max = int((y + h / 2) * height)
                            cv2.rectangle(image_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    st.image(image_cv, caption="带边界框的图像", use_column_width=True)
            else:
                st.write("未找到对应的标注文件")