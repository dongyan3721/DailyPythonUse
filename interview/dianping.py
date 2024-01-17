"""
@author David Antilles
@description 
@timeSnapshot 2024/1/17-01:34:49
"""
import random
import re
import sqlite3
import time
import pandas as pd

import bs4
import requests
from selenium import webdriver
from jwcATK.ProjectUtils import StringBuilder
from selenium.webdriver.common.by import By
from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader as PlainJsonReader
from bs4 import BeautifulSoup


class SpiderDomain:
    def __init__(self, name, preview, avgPirce, phone, address, reviewCount, star, url):
        self.name = name
        self.preview = preview
        self.avgPrice = avgPirce
        self.phone = phone
        self.address = address
        self.reviewCount = reviewCount
        self.star = star
        self.url = url


class ProxyHandler:
    def __init__(self):
        reader = PlainJsonReader("ips.json")
        self.ipList = reader.read("ips")
        self.total = len(self.ipList)

    def provide(self):
        # return {
        #     "https": f"https://{self.ipList[random.randint(0, self.total-1)]}",
        #     "http": f"http://{self.ipList[random.randint(0, self.total-1)]}"
        # }
        return {
            "https": "https://127.0.0.1:7890",
            "http": "http://127.0.0.1:7890"
        }


class DianPingSpider:
    def __init__(self):
        self.session = requests.session()
        self.reader = PlainJsonReader("dianpingproperties.json")
        self.chrome = webdriver.Chrome()
        self.chrome.get(self.reader.read("index"))
        self.proxyManager = ProxyHandler()
        time.sleep(15)
        """
        self.chrome.find_element(By.CLASS_NAME, value="user-opt-nologin").click()
        time.sleep(1)
        self.chrome.find_element(By.CLASS_NAME, value="bottom-password-login").click()
        time.sleep(3)
        self.chrome.find_element(By.ID, value="mobile-number-textbox").send_keys(self.reader.read("mobile_phone"))
        time.sleep(3)
        self.chrome.find_element(By.ID, value="pc-check").click()
        time.sleep(3)
        self.chrome.find_element(By.ID, value="send-vcode-button").click()
        captcha = input("验证码已发送，请输入")
        self.chrome.find_element(By.ID, value="number-textbox").send_keys(captcha)
        self.chrome.find_element(By.CLASS_NAME, value="button-pc").click()
        time.sleep(1)
        """
        self.chrome.refresh()
        self.cookie = self._parseCookie()
        print(self.cookie)
        # self.chrome.quit()
        # self.cookie = "WEBDFPID=910wu0u1xuw854xzzzz6510ux9vzy21881w831x88w8979583u7x4344-2020840294932-1705480294151SGIAKIEfd79fef3d01d5e9aadc18ccd4d0c95071121; _lxsdk_s=18d168c0e9f-ce8-e52-12f%7C%7C13; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk=18d168c0e9fc8-008660e990bfc4-26001951-1fa400-18d168c0e9fc8; dplet=254ae69ce878820ada0c5d0c618237dc; qruuid=734aa992-f16f-46d6-b736-95b4df3f283b; dper=0202032492f9ddcefa96eb734dbfb97b20663c3423da4f0625471dffec9c2a89ce0b5945604221697c3c7deab5f1b3865f1d29f0de0f62a6b62f00000000541d00001a3ff773bef009678685155a361352dad65e32957eac534ef9e0ac8ea3d09f41e5ae578fc2e1bae828f8b03a2913c6d4; _hc.v=89e91536-5506-0b6f-dcfd-9883da1bf1a0.1705480295; cye=shanghai; ua=%E7%BE%A7%E5%9F%BA%E7%BE%9F%E5%9F%BA%E5%B9%B2%E6%B0%A8%E5%9F%BA; ctu=5c534450ba214e1bce48f28a7d9ee65660ffe989e1beca038daac6a2dd96cfa7; fspop=test; _lxsdk_cuid=18d168c0e9fc8-008660e990bfc4-26001951-1fa400-18d168c0e9fc8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1705480300; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1705480309; cy=1"

    def _parseCookie(self):
        sb = StringBuilder()
        for item in reversed(self.chrome.get_cookies()):
            sb.add(item["name"])
            sb.add("=")
            sb.add(item["value"])
            sb.add("; ")

        return sb.toString()[:-2]

    def parseGeneral(self, url):
        headers = self.reader.read("general_header")
        headers["Cookie"] = self.cookie
        # self.chrome.get(url)
        # source = BeautifulSoup(self.chrome.page_source, "lxml")
        source = BeautifulSoup(self.session.get(url=url, headers=headers).text, "lxml")
        # source = BeautifulSoup(self.session.get(url=url, headers=headers, proxies=self.proxyManager.provide()).text, "lxml")
        shops: bs4.ResultSet = source.select(".shop-list ul li")
        domain = []
        for shop in shops:
            preview_img = shop.select_one(".pic a img")
            detail_url = shop.select_one(".pic a")["href"]
            preview = preview_img["src"]
            # 效果一样
            name = preview_img["title"]
            # 可以获取人均、评论条数和星级
            comment_div = shop.select_one(".comment")
            star = eval(re.findall("star_([0-9]+)", str(comment_div.select_one(".star")))[0]) / 10
            try:
                avg_price = comment_div.select_one(".mean-price b").string
            except:
                avg_price = '未知'
            print(comment_div.select_one("a").select_one("b").string)
            review_count = comment_div.select_one("a").select_one("b").string
            addr_tel = self._parseDetail(detail_url)
            address = addr_tel['address']
            phone = addr_tel["tel"]
            domain.append(SpiderDomain(name, preview, avg_price, phone, address, review_count, star, detail_url))
        return domain

    def _parseDetail(self, url):
        headers = self.reader.read("detail_header")
        headers["Cookie"] = self.cookie
        # source = BeautifulSoup(self.session.get(url=url, headers=headers, proxies=self.proxyManager.provide()).text, "lxml")
        source = BeautifulSoup(self.session.get(url=url, headers=headers).text, "lxml")
        # self.chrome.get(url)
        # source = BeautifulSoup(self.chrome.page_source, "lxml")
        # if str(source.select("title")).__contains__("403"):
        #     self.chrome = webdriver.Chrome()
        #     self.chrome.get(self.reader.read("index"))
        #     time.sleep(15)
        #     self.chrome.refresh()
        #     self.cookie = self._parseCookie()
        #     self.chrome.quit()
        #     headers["Cookie"] = self.cookie
        #     print("cookie-change")
        #     print(self.cookie)
        #     source = BeautifulSoup(self.session.get(url=url, headers=headers).text, "lxml")
        try:
            address = source.select_one("#address").string
        except:
            address = "未知地址"
        # print(str(source.select_one("#basic-info")))
        try:
            tel = re.findall("([0-9-]{8,})", str(source.select_one("#basic-info")))[0]
        except:
            tel = '未知电话'
        # time.sleep(random.randint(1, 3))
        return {"address": address, "tel": tel}


def exportToPersistence(data, columns, tableName):
    conn = sqlite3.connect("gen_shin")
    table = pd.DataFrame(data)
    try:
        table.columns = columns
    except:
        table = table.T
        table.columns = columns
    table.to_excel(tableName + ".xlsx")
    table.to_sql(tableName, conn, index=False, if_exists="replace")


if __name__ == '__main__':
    spider = DianPingSpider()
    res = []
    for i in range(10):
        s = spider.parseGeneral(
            f"https://www.dianping.com/search/keyword/1/0_上海酒吧/p{i + 1}")
        res += s
    xlsx = [[domain.name, domain.preview, domain.avgPrice, domain.phone,
             domain.address, domain.reviewCount, domain.star, domain.url] for domain in res]
    exportToPersistence(xlsx, ["name", "preview", "avg_price", "phone", "address",
                               "review_count", "star", "url"], "ShangHaiBar")
