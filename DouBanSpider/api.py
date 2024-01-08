import json
import re
from bs4 import BeautifulSoup
import pandas
import requests
from selenium import webdriver

from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader


class DuBanGrabber:
    def __init__(self):
        self.reader = DoubtfulJsonReader("settings.json")
        # self.session = requests.Session()
        self.maxPageNum = 5
        self.contentBuffer = []
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        driver = webdriver.Chrome(options=option)
        self.browser = driver

    def grab(self):
        baseRequestUrl = self.reader.read("base-url")
        for i in range(self.maxPageNum):
            requestUrl = f'{baseRequestUrl}&page_limit=50&page_start={i}'
            self.browser.get(requestUrl)
            content = re.findall("{\"subjects\":.+}]}", self.browser.page_source)[0]
            infoList = json.loads(content)["subjects"]
            outer = []
            for j in infoList:
                tempList = []
                detail = self.getDetail(j["url"])
                tempList.append(j["title"])
                tempList.append(j["rate"])
                for k in range(len(detail)):
                    tempList.append(detail[k])
                outer.append(tempList)
            self.contentBuffer.append(outer)

    def getDetail(self, url):
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        allInfo = str(soup.select("#info"))
        kind = re.findall("property=\"v:genre\">(.+?)</span>", allInfo)
        pl = re.findall("directedBy\">(.+?)</a>", allInfo)
        actress = re.findall(">(.+?)</a>", str(soup.select(".actor .attrs a")))
        print(url)
        ls = re.findall("<span><span class=\"pl\">编剧</span>.+?<br/>", allInfo)
        if len(ls) != 0:
            bookerHTML = ls[0]
            innerSoup = BeautifulSoup(bookerHTML, "lxml")
            bookers = re.findall(">(.+?)</a>", str(innerSoup.select(".attrs a")))
        else:
            bookers = []
        retList = [str(pl), str(bookers), str(actress), str(kind)]
        print(retList)
        return retList

    def export(self):
        for i in range(self.maxPageNum):
            data = pandas.DataFrame(self.contentBuffer[i])
            data.columns = ["影片名", "评分", "导演", "编剧", "主演", "类别"]
            data.to_excel(f"{i}.xlsx", index=False)
