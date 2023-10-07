

from pandas_profiling import ProfileReport

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns

def xml_to_csv(path):
    """Iterates through all .xml files (generated by labelImg) in a given directory and combines them in a single Pandas datagrame.

    Parameters:
    ----------
    path : {str}
        The path containing the .xml files
    Returns
    -------
    Pandas DataFrame
        The produced dataframe
    """
    classes_names = []
    xml_list = []
    for xml_file in glob.glob(path + "/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            classes_names.append(member[0].text)
            value = (
                root.find("filename").text,
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text),
            )
            xml_list.append(value)
    column_name = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return xml_df, classes_names

# 主运行函数
def run(inputDir,outputFile,labelMapDir):
    if inputDir is None:
        inputDir = os.getcwd()
    if outputFile is None:
        outputFile = inputDir + "/labels.csv"

    os.makedirs(os.path.dirname(outputFile), exist_ok=True)
    xml_df, classes_names = xml_to_csv(inputDir)
    xml_df.to_csv(outputFile, index=None)
    print("Successfully converted xml to csv.")
    if labelMapDir:
        os.makedirs(labelMapDir, exist_ok=True)
        label_map_path = os.path.join(labelMapDir, "label_map.pbtxt")
        print("Generate `{}`".format(label_map_path))

        # Create the `label_map.pbtxt` file
        pbtxt_content = ""
        for i, class_name in enumerate(classes_names):
            pbtxt_content = (
                pbtxt_content
                + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(
                    i + 1, class_name
                )
            )
        pbtxt_content = pbtxt_content.strip()
        with open(label_map_path, "w") as f:
            f.write(pbtxt_content)

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
        print("json_data: ", json_data)
        # As a file
        profile.to_file("your_report.json")
    elif file_type == 'jupyter':
        # jupyernotebook分析报告生成
        profile.to_widgets()
        profile.to_notebook_iframe()

if __name__ == '__main__':
    inputDir = '/Users/gatilin/Downloads/voc128/Annotations'
    outputFile = '/Users/gatilin/Downloads/voc128/Annotations.csv'
    labelMapDir = '/Users/gatilin/Downloads/voc128/Annotations'
    run(inputDir, outputFile, labelMapDir)

    file_name = '/Users/gatilin/Downloads/voc128/Annotations.csv'
    file_type = 'json'
    generate_profile_pandas(file_name, file_type)




