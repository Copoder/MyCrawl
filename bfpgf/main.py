root_url = 'https://www.fulixiu.vip/yld/page'
import crawler

if __name__ == '__main__':
    crawl = crawler.Requester(root_url, "")  # param2 key_word
    crawl.start()
