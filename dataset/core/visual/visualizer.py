import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# # %matplotlib inline

def my_autopct(pct):
    return ('%.2f%%' % pct) if pct > 2 else ''



df_data = pd.read_csv('/home/hxzh02/图片/Annotations.csv')
print(df_data.info())
print(df_data.describe())

sample_for_plotting = df_data[['width','height','class', 'xmin','ymin','xmax','ymax']]
data_head = sample_for_plotting.head()

# plotting_group = sample_for_plotting.groupby('Product')
print('data_head:\n', data_head)

plotting_group= sample_for_plotting.groupby('class')
data_class_head = plotting_group.head()
print('data_class_head:\n', data_class_head)

data_xmin = df_data.groupby('class').mean()['xmin']
print('data_xmin:\n', data_xmin)

data_ymin = df_data.groupby('class').mean()['ymin']
print('data_ymin:\n', data_ymin)

data_xmax = df_data.groupby('class').mean()['xmax']
print('data_xmax:\n', data_ymin)

data_ymax = df_data.groupby('class').mean()['ymax']
print('data_ymax:\n', data_ymin)

# 计算class标记频次
count = pd.value_counts(df_data['class'])
print('count:\n', count)

# _ = plt.hist(count)
# plt.imshow(_)


# 最简单，只传递x，组数，宽度，范围
plt.hist(df_data['class'], bins=34, rwidth=10, range=(1,34), align='left')
plt.show()
# words = df_data.class.value_counts()
# print(words)

# print(df['gender'].value_counts()/df['gender'].count()*100)   #Gender statistics


plt.figure(figsize=(8,5), dpi=80)
# 拿参数接收hist返回值，主要用于记录分组返回的值，标记数据标签
n, bins, patches = plt.hist(df_data['class'], bins=34, rwidth=10, range=(1,34), align='left', label='xx直方图')
for i in range(len(n)):
    plt.text(bins[i], n[i]*1.02, int(n[i]), fontsize=12, horizontalalignment="center") #打标签，在合适的位置标注每个直方图上面样本数
plt.ylim(0,1000)
plt.title('image')
plt.legend()
# plt.savefig('直方图'+'.png')
plt.show()
