import requests,queue,threading,os

Headers = {
    "Accept" : "application/json, text/plain, */*",
    "Origin" : "https://wx.zsxq.com",
    "Referer" : "https://wx.zsxq.com/dweb/",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Cookie" : "UM_distinctid=16ba358324e9cf-0b3bdbe3103e0c-e323069-1fa400-16ba358324fdd0; zsxq_access_token=019E2596-DBBC-2C7B-59B1-59AFA8FA540B"
}

Base_url = 'https://api.zsxq.com/v2/groups/{}/files?count=48&{}'
Download_url = 'https://api.zsxq.com/v2/files/{}/download_url'
# https://api.zsxq.com/v2/files/118212181584482/download_records?count=48
Download_file_queue = queue.Queue()
thread_list = []
THREADS = 2
ID = '222452455121'

class Download_th(threading.Thread):
    def __init__(self):
        super(Download_th,self).__init__()
    
    def run(self):
        while not Download_file_queue.empty():
            file_info = Download_file_queue.get()
            print('正在下载：'+file_info[1])
            while True:
                try:
                    r = requests.get(Download_url.format(file_info[0]),headers = Headers,timeout=(5,30))
                    download_link = r.json()['resp_data']['download_url']
                    with open(os.getcwd() + '\\files\\' + file_info[1],'wb') as file_save:
                        r = requests.get(download_link,headers = Headers)
                        r.raise_for_status()
                        for chunk in r.iter_content(100000):
                            file_save.write(chunk)
                    break
                except:
                    pass

def req(endtime=''):
    r = requests.get(Base_url.format(ID,endtime),headers=Headers)
    return r.json()

def load_files():
    end_time = ''
    status = True
    while status:
        json_data = req(end_time)
        file_list = json_data['resp_data']['files']
        if file_list != []:
            for download_file in file_list:
                Download_file_queue.put([download_file['file']['file_id'],download_file['file']['name']])
            else:
                create_time = download_file['file']['create_time']
                print('完成日期：' + create_time)
                end_time = create_time[:-8] + str(int(create_time[-8:-5])-1).zfill(3) + create_time[-5:]
                end_time = 'end_time=' + end_time.replace(':','%3A').replace('+','%2B')
        else:
            status = False
            print('读取全部file完毕')

if __name__ == '__main__':
    load_files()
    for x in range(THREADS):
        th = Download_th()
        thread_list.append(th)
        th.start()
    for th_ in thread_list:
        th_.join()