import requests
from ProjectApis import *
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
import json

location_sup = {"上海": "sh", "苏州": "su", "杭州": "hz", "宁波": "nb", "南京": "nj"}
fp = open('signal.json', mode="r", encoding="GBK")
city = json.load(fp)["city"]
fp.close()

if city[-1] == "市":
    location = location_sup[city[:-1]]
else:
    location = location_sup[city]


urlHead = "https://"
urlBody = ".zu.anjuke.com/fangyuan/p"
urlTail = "/?kw=&k_comm_id="

headers = {
    'Accept': "application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 '
                  'Safari/537.36',
    'cookie': "SECKEY_ABVK=+kqXYId+nmOrh1WP+rSr5+oUr3AHMPEYONnHPlrHM0g%3D; "
               "BMAP_SECKEY=OnJNoqU92iChkrnl7rVoVnfJxPbP0h_74QCnUQupKM-BdVocMJLv9DSTGatot2Q4twAanimFOpm0xS"
               "-i31qQuhZ4AwUm1ABJZytRP32UjV92aKC-8l6wE5tLZLqqTg-VgEc9k4uRkhICe"
               "-KtAaAIjsKQ7xSaNGMB_NP11vymQ618t6cH1tF5dj9R55I1vtbA; "
               "aQQ_ajkguid=24BF0B7A-E0FD-90E6-A3E5-1DAAE5010A30; id58=CocNF2K1ajRyKr42BCxOAg==; "
               "58tj_uuid=2cdbb852-e5c1-4332-b462-d0ba9e3d4f24; als=0; wmda_new_uuid=1; "
               "wmda_uuid=28c78fcceedf0f86655568eb56e40ad0; wmda_visited_projects=%3B6289197098934; "
               "_ga=GA1.2.950265032.1656167372; ajk-appVersion=; "
               "fzq_h=7fd89fb00316928c46cd4ac015f9b346_1656512692361_2a5df7eb2a7f46c3bc637f1330edfea6_1699161488; "
               "sessid=E8CEBE9F-89D3-A60B-8957-BFEE3C673763; twe=2; _gid=GA1.2.1519383194.1656752171; "
               "lps=https%3A%2F%2Fsx.zu.anjuke.com%2F%3Fkw%3D%26k_comm_id%3D%7Chttps%3A%2F%2Fshaoxing.anjuke.com%2F"
               "%3Fpi%3DPZ-baidu-pc-all-biaoti; wmda_session_id_6289197098934=1656766456496-225fe4c8-4d1f-f654; "
               "ctid=66; cmctid=355; new_session=1; init_refer=; new_uv=10; obtain_by=1; "
               "xxzl_cid=e89a6e2a68344708af10e5481e0b2407; xzuid=9d432e44-fbaf-4ca1-808d-a1ed47ff52f "

}

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数

price = []  # 价格
des = []  # 描述
rooms = []  # X室X厅
area = []  # 面积
community = []  # 小区名
address = []  # 地址
link = []  # 详情页

for i in range(1, 20):
    htmlSource = ""
    while htmlSource == "":
        try:
            s = requests.session()
            s.keep_alive = False  # 关闭多余连接
            proxies = getProxy_file()
            print(f'ip this term: {proxies["https://"]}')
            resp = s.get(url=urlHead + location + urlBody + str(i) + urlTail, headers=headers, timeout=300, proxies=proxies)
            htmlSource = resp.text.replace("\n", "")

        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    price += getPriceInfo(htmlSource)
    des += getDescription(htmlSource)
    rooms += getRooms(htmlSource)
    area += getArea(htmlSource)
    community += getCommunityName(htmlSource)
    address += getLocation(htmlSource)
    link += getDetailedLinks(htmlSource)

data = pd.DataFrame([price, des, rooms, area, community, address, link],
                    index=["价格", "简述", "房屋配置", "房屋面积", "隶属小区", "地址", "详情页"])
# print(data)
engine = create_engine("mysql+pymysql://root:6666@127.0.0.1:3306/linktest?charset=utf8")
with engine.begin() as connect:
    data.T.to_sql(name=city, con=connect, if_exists="replace", index=False)
engine.dispose()

pf = open("flag.txt", "w")
pf.write("1")
pf.close()
