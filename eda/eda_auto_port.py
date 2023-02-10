
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

def generate_profile_pandas(file_names, file_type):
    # 读取数据
    df = pd.read_csv(file_names)
    # 数据分析
    profile = ProfileReport(df, title="Data Report", explorative=True)
    if file_type == 'html':
        # html分析报告生成
        profile.to_file("your_report.html")
    elif file_type == 'json':
        # json分析报告生成
        # As a JSON string
        json_data = profile.to_json()
        # As a file
        # profile.to_file("your_report.json")
    elif file_type == 'jupyter':
        # jupyernotebook分析报告生成
        profile.to_widgets()
        profile.to_notebook_iframe()

if __name__ == '__main__':


    file_name = '/home/linxu/Downloads/GoogleDownload/Annotations.csv'
    file_type = 'html'
    generate_profile_pandas(file_name, file_type)




