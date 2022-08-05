
# 调用一些需要的第三方库
import numpy as np
import pandas as pd
import shutil
import json
import os
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from matplotlib.font_manager import FontProperties
from PIL import Image
import random
myfont = FontProperties(size=12)
plt.rcParams['figure.figsize'] = (12, 12)

from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs


def get_all_bboxes(df, name):
    image_bboxes = df[df.file_name == name]

    bboxes = []
    categories = []
    for _, row in image_bboxes.iterrows():
        bboxes.append((row.bbox_xmin, row.bbox_ymin, row.bbox_w, row.bbox_h, row.category_id))
    return bboxes


def plot_image_examples(df, rows=3, cols=3, title='Image examples'):
    fig, axs = plt.subplots(rows, cols, figsize=(15, 15))
    color = ['#FFB6C1', '#D8BFD8', '#9400D3', '#483D8B', '#4169E1', '#00FFFF', '#B1FFF0', '#ADFF2F', '#EEE8AA',
             '#FFA500', '#FF6347']  # 各部分颜色
    for row in range(rows):
        for col in range(cols):
            idx = np.random.randint(len(df), size=1)[0]
            name = df.iloc[idx]["file_name"]
            img = Image.open(TRAIN_DIR + str(name))
            axs[row, col].imshow(img)

            bboxes = get_all_bboxes(df, name)
            for bbox in bboxes:
                rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor=color[bbox[4]],
                                         facecolor='none')
                axs[row, col].add_patch(rect)

            axs[row, col].axis('off')

    plt.suptitle(title, fontproperties=myfont)
    plt.show()

    def plot_gray_examples(df, rows=3, cols=3, title='Image examples'):
        fig, axs = plt.subplots(rows, cols, figsize=(15, 15))
        color = ['#FFB6C1', '#D8BFD8', '#9400D3', '#483D8B', '#4169E1', '#00FFFF', '#B1FFF0', '#ADFF2F', '#EEE8AA',
                 '#FFA500', '#FF6347']  # 各部分颜色
        for row in range(rows):
            for col in range(cols):
                idx = np.random.randint(len(df), size=1)[0]
                name = df.iloc[idx]["file_name"]
                img = Image.open(TRAIN_DIR + str(name)).convert('L')
                axs[row, col].imshow(img)

                bboxes = get_all_bboxes(df, name)
                for bbox in bboxes:
                    rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1,
                                             edgecolor=color[bbox[4]], facecolor='none')
                    axs[row, col].add_patch(rect)

                axs[row, col].axis('off')

        plt.suptitle(title, fontproperties=myfont)

    def hist_hover(dataframe, column, colors=["#94c8d8", "#ea5e51"], bins=30, title=''):
        """Count the appearance of values in one column and plot the histogram.
        """
        hist, edges = np.histogram(dataframe[column], bins=bins)

        hist_df = pd.DataFrame({column: hist,
                                "left": edges[:-1],
                                "right": edges[1:]})
        hist_df["interval"] = ["%d to %d" % (left, right) for left,
                                                              right in zip(hist_df["left"], hist_df["right"])]

        src = ColumnDataSource(hist_df)
        plot = figure(plot_height=400, plot_width=600,
                      title=title,
                      x_axis_label=column,
                      y_axis_label="Count")
        plot.quad(bottom=0, top=column, left="left",
                  right="right", source=src, fill_color=colors[0],
                  line_color="#35838d", fill_alpha=0.7,
                  hover_fill_alpha=0.7, hover_fill_color=colors[1])

        hover = HoverTool(tooltips=[('Interval', '@interval'),
                                    ('Count', str("@" + column))])
        plot.add_tools(hover)

        output_notebook()
        show(plot)


if __name__ == '__main__':

    # Setup the paths to train and test images
    TRAIN_DIR = '/media/hxzh02/SB@home/hxzh/Downloads/wheat/wheat/train/'
    TRAIN_CSV_PATH = '/media/hxzh02/SB@home/hxzh/Downloads/wheat/wheat/train.json'

    # 读取训练集标注文件
    with open(TRAIN_CSV_PATH, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    train_fig = pd.DataFrame(train_data['images'])

    train_fig_head = train_fig.head()
    print('train_fig_head:', train_fig_head)

    ps = np.zeros(len(train_fig))
    for i in range(len(train_fig)):
        ps[i] = train_fig['width'][i] * train_fig['height'][i] / 1e6
    plt.title('训练集图片大小分布', fontproperties=myfont)
    sns.histplot(ps, bins=21, kde=False)

    train_anno = pd.DataFrame(train_data['annotations'])
    df_train = pd.merge(left=train_fig, right=train_anno, how='inner', left_on='id', right_on='image_id')
    df_train['bbox_xmin'] = df_train['bbox'].apply(lambda x: x[0])
    df_train['bbox_ymin'] = df_train['bbox'].apply(lambda x: x[1])
    df_train['bbox_w'] = df_train['bbox'].apply(lambda x: x[2])
    df_train['bbox_h'] = df_train['bbox'].apply(lambda x: x[3])
    df_train['bbox_xcenter'] = df_train['bbox'].apply(lambda x: (x[0] + 0.5 * x[2]))
    df_train['bbox_ycenter'] = df_train['bbox'].apply(lambda x: (x[1] + 0.5 * x[3]))

    df_train['bbox_count'] = df_train.apply(lambda row: 1 if any(row.bbox) else 0, axis=1)
    train_images_count = df_train.groupby('file_name').sum().reset_index()
    less_spikes_ids = train_images_count[train_images_count['bbox_count'] > 50].file_name
    plot_image_examples(df_train[df_train.file_name.isin(less_spikes_ids)], title='单图目标超过50个（示例）')




