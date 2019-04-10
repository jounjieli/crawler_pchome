#!/usr/bin/env python
# coding: utf-8
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import chardet
from Model import crawler
from View import Get_the_spoils

class control_spider():
    @classmethod
    def create_spider(cls,session=True):
        spider = crawler()
        if session == True:
            sess = spider.create_session()
        return spider
    @classmethod
    def search_pchome_title(cls):
        url = "https://www.pcstore.com.tw/adm/psearch.htm"
        key_word = input('輸入關鍵字:')
        key_word = key_word.encode("big5-hkscs")
        params = {"store_k_word":key_word,'slt_k_option':"1",'page_count': "40"}
        spider = cls.create_spider(session=False)
        spider.sess_post_url(url,data=params)
        soup = spider.get_soup(encoding="big5-hkscs")
        title_soup = soup.find_all("div",re.compile("pic2t "))
        title_list = []
        for index, item in enumerate(title_soup):
            title_list.append("{0:2d}. {1}".format(index + 1, item.text.strip()))
        Get_the_spoils.print_list(title_list)
        spider.save_res("test.html","big5-hkscs")
        return title_list

if __name__ == "__main__":
    spider = control_spider.search_pchome_title()
