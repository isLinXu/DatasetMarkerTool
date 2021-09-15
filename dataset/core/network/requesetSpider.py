import requests
import os
import re


def get_images_from_baidu(keyword, page_num, save_dir):
    '''
    伪装浏览器爬取图片
    :param keyword:
    :param page_num:
    :param save_dir:
    :return:
    # 实现原理
    # UA 伪装：当前爬取信息伪装成浏览器
    # 将 User-Agent 封装到一个字典中
    # 【（网页右键 → 审查元素）或者 F12】 → 【Network】 → 【Ctrl+R】 → 左边选一项，右边在 【Response Hearders】 里查找
    '''

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    # 请求的 url
    url = 'https://image.baidu.com/search/acjson?'
    n = 0
    for pn in range(0, 30 * page_num, 30):
        print('开始请求数据...')
        # 请求参数
        param = {'tn': 'resultjson_com',
                 # 'logid': '7603311155072595725',
                 'ipn': 'rj',
                 'ct': 201326592,
                 'is': '',
                 'fp': 'result',
                 'queryWord': keyword,
                 'cl': 2,
                 'lm': -1,
                 'ie': 'utf-8',
                 'oe': 'utf-8',
                 'adpicid': '',
                 'st': -1,
                 'z': '',
                 'ic': '',
                 'hd': '',
                 'latest': '',
                 'copyright': '',
                 'word': keyword,
                 's': '',
                 'se': '',
                 'tab': '',
                 'width': '',
                 'height': '',
                 'face': 0,
                 'istype': 2,
                 'qc': '',
                 'nc': '1',
                 'fr': '',
                 'expermode': '',
                 'force': '',
                 'cg': '',  # 这个参数没公开，但是不可少
                 'pn': pn,  # 显示：30-60-90
                 'rn': '30',  # 每页显示 30 条
                 'gsm': '1e',
                 '1618827096642': ''
                 }
        request = requests.get(url=url, headers=header, params=param)
        if request.status_code == 200:
            print('请求成功 Request success.')
        request.encoding = 'utf-8'

        # 正则方式提取图片链接
        html = request.text
        image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
        print(image_url_list)

        # # 换一种方式
        # request_dict = request.json()
        # info_list = request_dict['data']
        # # 看它的值最后多了一个，删除掉
        # info_list.pop()
        # image_url_list = []
        # for info in info_list:
        #     image_url_list.append(info['thumbURL'])

        # 创建文件目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 遍历图片列表,保存图片到指定路径
        for image_url in image_url_list:
            image_data = requests.get(url=image_url, headers=header).content
            with open(os.path.join(save_dir, f'{n + 1:06d}.jpg'), 'wb') as fp:
                fp.write(image_data)
            n = n + 1

    print('所有图片请求结束')



if __name__ == '__main__':
    # 设置搜索-关键字
    # keywords = ['输电塔', '输电塔架', '猫塔', '电力输电塔架', '干字塔', '酒杯塔', '官帽塔', '单回路塔', '双回路塔']
    # keywords = ['灾后电塔','杆塔倒塌','铁塔倒塌']
    keywords = ['电网铁塔', '电塔']
    for keyword in keywords:
        save_dir = "/home/hxzh02/文档/PlanetDataset/src/" + keyword
        page_num = 100
        get_images_from_baidu(keyword, page_num, save_dir)
        print('Get images finished.')
