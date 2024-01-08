import requests
import re
import time
import datetime
import io
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader as PlainJsonReader
from bs4 import BeautifulSoup


class CaptchaSelector:
    def __init__(self, url: str):
        self.url = url

    def parse(self, jsonReader: PlainJsonReader, headers: dict):
        content = requests.get(url=self.url, headers=headers).content
        with open(jsonReader.read("local_captcha_name"), "wb+") as f:
            f.write(content)
            f.close()


class LoginModel:
    def __init__(self):
        self.__browser = webdriver.Chrome("./chromedriver.exe")
        self.__reader = PlainJsonReader("application.json")
        self.__stringBuilder = io.StringIO()

    def __cookieQuery(self):
        return self.__browser.get_cookies()

    def __buildCookie(self, key: str, value: str):
        self.__stringBuilder.write(key)
        self.__stringBuilder.write("=")
        self.__stringBuilder.write(value)
        self.__stringBuilder.write(";")

    def __cookieOutput(self, browserCookie):
        for cookie in browserCookie:
            self.__buildCookie(cookie["name"], cookie["value"])
        cookie = self.__stringBuilder.getvalue()[0: -1]
        self.__stringBuilder = io.StringIO()
        return cookie

    def login(self):
        self.__browser.get(self.__reader.read("index"))
        time.sleep(2)
        accountInputBox = self.__browser.find_element(By.ID, "loginId")
        passwordInputBox = self.__browser.find_element(By.ID, "password")
        captchaInputBox = self.__browser.find_element(By.ID, "yzm")
        submitButton = self.__browser.find_element(By.ID, "subBut")
        accountInputBox.send_keys(self.__reader.read("account"))
        passwordInputBox.send_keys(self.__reader.read("password"))

        cookies = self.__cookieQuery()

        cookie = self.__cookieOutput(cookies)
        htmlContent = self.__browser.page_source
        soup = BeautifulSoup(htmlContent, "lxml")
        captchaComponent = soup.select("#codeImage")
        captchaUrl = re.findall("src=\"(.+?)\"", str(captchaComponent))[0]
        captchaDownloader = CaptchaSelector(captchaUrl)
        print(captchaUrl)
        getImageHeaders = self.__reader.read("captcha_image_headers")
        getImageHeaders["Cookie"] = cookie
        captchaDownloader.parse(self.__reader, getImageHeaders)
        captcha_value = input("请输入同目录下{}的值...".format(self.__reader.read("local_captcha_name")))
        captchaInputBox.send_keys(captcha_value)
        submitButton.click()

    def getRequestCookie(self):
        time.sleep(3)
        self.__browser.get(self.__reader.read("center"))
        time.sleep(2)
        self.__browser.refresh()
        return self.__cookieOutput(self.__cookieQuery())


class DataGrabber:
    def __init__(self, cookie):
        self.cookie = cookie
        self.reader = PlainJsonReader("application.json")

    def grabWholeCollege(self):
        headers = self.reader.read("query_whole_college_headers")
        headers["Cookie"] = self.cookie
        data = {
            "queryLeagueId": self.reader.read("top_league_id")
        }
        resp = requests.post(url=self.reader.read("query_whole_college_url"), headers=headers, data=data)
        print(resp.json())
        respData = resp.json()["results"]["leagueList"]
        print(respData)
        column = ["支部id", "支部名称", "支部全称", "支部类型", "是否叶子节点"]
        ids = []
        simplifiedNames = []
        wholeNames = []
        leagueType = []
        isLeafNode = []
        for item in respData:
            ids.append(item["leagueId"])
            simplifiedNames.append(item["leagueName"])
            wholeNames.append(item["leagueFullName"])
            leagueType.append(item["leagueTypeId"])
            isLeafNode.append(item["isLeaf"])
        xls = pd.DataFrame([ids, simplifiedNames, wholeNames, leagueType, isLeafNode])
        xls = xls.T
        xls.columns = column
        xls.to_excel("【更新{}】光电学院团支部明细.xlsx".format(datetime.date.today()))


if __name__ == '__main__':
    login = LoginModel()
    login.login()
    print(login.getRequestCookie())
    grabber = DataGrabber(login.getRequestCookie())
    grabber.grabWholeCollege()
    
