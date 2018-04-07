from urllib import request
from bs4 import BeautifulSoup
import customparser
import Constans


class Requester:
    def __init__(self, root_url, key_word):
        self.page_count = 370
        self.cur_page = 1
        self.root_url = root_url
        self.parser = customparser.Parser(key_word)

    def start(self):
        self.root_page_crawler()

    def root_page_crawler(self):
        # 一层总页数控制，并负责进入二级页面
        cur_url = self.root_url + self.cur_page.__str__()
        print(cur_url)
        self.cur_page = self.cur_page + 1
        root_req = request.Request(cur_url, headers=Constans.HEADERS)
        with request.urlopen(root_req) as r:
            if r.status == 200 and r.reason == 'OK':
                # 拿到当前二级页面入口list,list全部检索完毕后递归
                while self.cur_page != self.page_count + 1:
                    self.parser.root_parse(r.read())
                    self.root_page_crawler()
            else:
                print("ERROR")
                self.root_page_crawler()
