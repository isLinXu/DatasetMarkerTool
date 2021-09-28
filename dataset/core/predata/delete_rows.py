import os
import pandas as pd
#delete_row：清洗数据，解决csv文件和数据集标签有些对不上
df = pd.read_csv('data/train.csv')
print(df)
IMG = "data/train"
file = pd.DataFrame([i.split('.')[0] for i in os.listdir(IMG)], columns=['image_id'])
exists = file.drop_duplicates()
df = pd.merge(exists, df, on='image_id')


submission = pd.DataFrame(df)
submission.to_csv('train.csv', index=False)
