import requests
import re
from bs4 import BeautifulSoup
import parsel
import numpy as np


def getProxy_file():
    fp = open("ips.txt", "r")
    li = fp.readlines()
    std =  []
    for i in range(44):
        std.append(li[i].replace("\n", ""))
    index = np.random.randint(0, 43)
    proxy = std[index]
    proxies = {
        "http://": proxy,
        "https://": proxy
    }
    return proxies


def getProxy_Json(url):
    resp = requests.get(url)
    ip = resp.json()['data'][0]
    proxy = ip['ip'] + ':' + str(ip['port'])
    proxies = {
        "http://": proxy,
        "https://": proxy
    }
    return proxies


def getProxy_PlainText(url):
    resp = requests.get(url)
    ip = re.findall("([0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}):", resp.text)[0]
    port = re.findall(":([0-9]+)", resp.text)[0]
    proxy = ip + ":" + port
    proxies = {
        "http://": proxy,
        "https://": proxy
    }
    return proxies


def getDetailedLinks(htmlSourceFile):  # ok
    selector = parsel.Selector(htmlSourceFile)
    hrefLinks = selector.css(".img::attr(href)").getall()
    return hrefLinks


def getPriceInfo(htmlSourceFile):  # ok
    priceList = []
    soup = BeautifulSoup(htmlSourceFile, "lxml")
    temp = soup.find_all(attrs={"class": "zu-side"})
    for price in temp:
        priceList.append(str(price.p.strong.b.string))
    return priceList


def getDescription(htmlSourceFile):  # ok
    desList = []
    soup = BeautifulSoup(htmlSourceFile, "lxml")
    temp = soup.find_all(attrs={"class": "zu-info"})
    for des in temp:
        desList.append(str(des.h3.a.b.string))
    return desList


def getRooms(htmlSourceFile):  # ok
    end = []
    room1 = re.findall(">([0-9]+)</b>室", htmlSourceFile)
    room2 = re.findall(">([0-9]+)</b>厅", htmlSourceFile)
    for i, j in zip(room1, room2):
        end.append(i + "室" + j + "厅")
    return end


def getArea(htmlSourceFile):  # ok
    area = re.findall(">([0-9\.]+)</b>平米", htmlSourceFile)
    end = []
    for i in area:
        end.append(i + "平米")
    return end


def getCommunityName(htmlSourceFile):  # ok
    name = []
    nam2 = []
    soup = BeautifulSoup(htmlSourceFile, "lxml")
    temp = soup.find_all(attrs={"class": "details-item"})
    for name_p in temp:
        name.append(name_p.a)

    for n in name:
        if len(str(n)) != 4:  # bs4的bug：解析class名字带空格只能解析到空格之前
            nam2.append(str(BeautifulSoup(str(n), "lxml").string))
    return nam2


def getLocation(htmlSourceFile):  # ok
    pl = []
    location = re.findall("</a>&nbsp;&nbsp;(.+?)</address>", htmlSourceFile)
    for p in location:
        pl.append(p.strip())
    return pl


if __name__ == '__main__':
    fp = open("dest.txt", "r", encoding='utf-8')
    content = fp.read().replace("\n", "")
    print(getLocation(content))