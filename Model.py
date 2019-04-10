#!/usr/bin/env python
# coding: utf-8
import requests
import html5lib
from bs4 import BeautifulSoup
import re
import chardet

class crawler():
    response = None
    session = None
    def __init__(self,headers = None, cookies = None, proxies = None):
        self.set_default_parameter()
        if headers != None:
            self.headers = self.headers_to_dict(headers)
        if cookies != None:
            cookies_dict = self.cookies_to_dict(cookies)
            self.cookies = cookies_dict
        if proxies != None:
            self.proxies = proxies
        self.update_parameter()

    def set_default_parameter(self):
        #default
        self.headers = {
            'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
            ,"referer":"https://www.pcstore.com.tw/"
            ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.cookies = None
        self.proxies = None

    def update_parameter(self):
        parameter = {}
        if self.headers != None:
            parameter.update({'headers':self.headers})
        if self.cookies != None:
            parameter.update({'cookies':self.cookies})
        if self.proxies != None:
            parameter.update({'proxies':self.proxies})
        self.parameter = parameter

    def set_parameter(self,headers = None, cookies = None, proxies = None):
        """arg = 'None'，parameter clears"""
        if headers != None:
            self.headers = self.headers_to_dict(headers)
            if headers == "None":
                self.headers = None
        if cookies != None:
            self.cookies = self.cookies_to_dict(cookies)
            if cookies == "None":
                self.cookies = None
        if proxies != None:
            self.proxies = proxies
            if proxies == "None":
                self.proxies = None
        self.update_parameter()

    @classmethod
    def cookies_to_dict(cls,cookie):
        """cookies(str) to cookies(dict)"""
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        return cookies
    @classmethod
    def headers_to_dict(cls,header):
        """headers(str) to headers(dict)"""
        return dict(line.split(": ", 1) for line in header.split("\n"))

    def create_session(self):
        sess = requests.Session()
        self.session = sess

    def sess_get_url(self,url, **get_parameter):
        """get_parameter input: params,timeout..."""
        if self.session == None:
            self.create_session()
        sess = self.session
        parameter = self.parameter
        response = sess.get(url, **parameter, **get_parameter)
        self.response = response

    def sess_post_url(self,url, **get_parameter):
        if self.session == None:
            self.create_session()
        sess = self.session
        parameter = self.parameter
        response = sess.post(url, **parameter, **get_parameter)
        self.response = response

    def get_url(self, url, **get_parameter):
        """get_parameter input: params,timeout..."""
        parameter = self.parameter
        response = requests.get(url, **parameter, **get_parameter)
        self.response = response

    def post_url(self,url, encoding=None, **get_parameter):
        parameter = self.parameter
        response = requests.post(url, **parameter, **get_parameter)
        self.response = response

    def get_soup(self,encoding=None):
        response = self.response.text
        if encoding != None:
            response = self.response.content.decode(encoding,'ignore')
        soup = BeautifulSoup(response, "html5lib")
        return soup

    def save_res(self,path,encoding):
        res_write = self.response.content.decode(encoding,'ignore')
        with open(path,'w',encoding=encoding) as f:
            f.write(res_write)
