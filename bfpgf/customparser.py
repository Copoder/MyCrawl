from bs4 import BeautifulSoup
import re
from urllib import request
from bs4 import BeautifulSoup
import os
import Constans
import FileLogHelper
from datetime import datetime, timedelta


def down_load(name, path, content):
    if not os.path.exists(path):
        os.mkdir(path)
    temp_file = open(path + '/' + name, 'wb')
    temp_file.write(content)
    temp_file.close()


class Parser:
    def __init__(self, key_word):
        self.key_word = key_word
        self.item_count = 0

    def root_parse(self, html):
        self.bs_manager = BeautifulSoup(html, 'html.parser')
        # \d+为目标 外层列表页
        datas = self.bs_manager.find_all('a', attrs={"href": re.compile('https://www.fulixiu.vip/yld/\d+.html')})
        for b in datas:
            if self.key_word in b.get_text():
                name = b.get_text()
                link = b['href']
                print(name, link)
                self.second_parse(link, name)

    def second_parse(self, link, name):
        self.item_count = 0
        req = request.Request(link, headers=Constans.HEADERS)
        # 二级页面,方法内控制页面切换,将解析和下载工作交给save方法
        with request.urlopen(req) as r:
            item_path = Constans.ROOT_PATH + name
            if r.status == 200 and r.reason == 'OK':
                start = datetime.now()
                bs_manager = BeautifulSoup(r.read(), 'html.parser')
                pages = bs_manager.find_all('a', attrs={'href': re.compile(link + '/\d')})
                page_count = 0
                if not os.path.exists(item_path):
                    os.mkdir(item_path)
                FileLogHelper.write_log_with_time(item_path, 'log', 'start:' + name)
                for page in pages:
                    print(page['href'])
                    self.save(page['href'], item_path, self.item_count)
                    page_count = page_count + 1

            stop = datetime.now()
            date_data = (stop - start).total_seconds()
            FileLogHelper.write_log_with_time(item_path, 'log', 'end:耗时' + str(date_data))
            FileLogHelper.write_log_with_time(item_path, 'log', '共计项目' + str(self.item_count) + '个')

    def save(self, img_url, path, item_count):
        req = request.Request(img_url, headers=Constans.HEADERS)
        with request.urlopen(req) as r:
            if r.status == 200 and r.reason == 'OK':
                read = r.read()
                bs = BeautifulSoup(read, 'html.parser')
                imgs = bs.find_all('img', src=re.compile('.jpg$'))
                # TODO 简化这一操作,太繁琐
                img_set = set()
                for item in imgs:
                    img_set.add(item)

                for img in img_set:
                    print("下载项：" + img['src'])
                    req = request.Request(img['src'], headers=Constans.HEADERS)
                    with request.urlopen(req) as rs:
                        if rs.status == 200 and rs.reason == 'OK':
                            down_load(self.item_count.__str__() + '.jpg', path, rs.read())
                            self.item_count = self.item_count + 1
