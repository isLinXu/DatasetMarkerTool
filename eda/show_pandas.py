import sweetviz as sv
import pandas as pd

if __name__ == '__main__':

    file_name = '/home/hxzh02/图片/Annotations.csv'

    # 读取数据
    df = pd.read_csv(file_name)
    my_report = sv.analyze(df)
    # Default arguments will generate to "SWEETVIZ_REPORT.html"
    my_report.show_html()