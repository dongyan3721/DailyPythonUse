import requests
from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader
import os
import shutil
import uuid
import pandas
from sqlalchemy import create_engine
from urllib.parse import quote_plus as url_parser


def copy_and_rename_file(source_dir, target_dir, file_name, new_file_name):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    source_file_path = os.path.join(source_dir, file_name)
    target_file_path = os.path.join(target_dir, new_file_name)

    if os.path.exists(source_file_path):
        shutil.copy(source_file_path, target_file_path)
        print(f"File {source_file_path} copied to {target_file_path}")
    else:
        print(f"File {file_name} does not exist in {source_dir}.")


class DownLoader:
    def __init__(self, session: requests.Session):
        self.session = session

    def _write(self, content, filename):
        with open(filename, "wb+") as f:
            f.write(content)
            f.close()

    def download(self, uuid: str, storageType: int, url: str):
        resp = self.session.get(url=url)
        text = resp.text
        if text.__contains__("html"):
            if storageType == 0:
                copy_and_rename_file(".", "./avatar", "fail.jpg", uuid + ".jpg")
            elif storageType == 1:
                copy_and_rename_file(".", "./preview", "fail.jpg", uuid + ".jpg")
            else:
                copy_and_rename_file(".", "./content", "fail.png", uuid + ".mkv")
            return False
        else:
            content = resp.content
            if storageType == 0:
                self._write(content=content, filename="./avatar/" + uuid + ".jpg")
            elif storageType == 1:
                self._write(content, "./preview/" + uuid + ".jpg")
            else:
                self._write(content, "./content/" + uuid + ".mp4")
            return True


class VideoMessageGrabber:
    def __init__(self):
        self.reader = DoubtfulJsonReader("settings.json")
        self.session = requests.session()
        self.title = []
        self.author = []
        self.description = []
        self.content = []
        self.avatar = []
        self.preview = []
        self.uuid = []

    def grabVideo(self, maxCount: int):
        baseUrl = "https://localhost:8080/getRes/"
        downloader = DownLoader(self.session)
        requestUrl = self.reader.read("base-url")
        requestHeader = self.reader.read("headers")
        for i in range(maxCount):
            content = self.session.get(url=requestUrl, headers=requestHeader).json()["result"]["list"]
            for j in range(len(content)):
                print(j + 1 + i * len(content))
                self.title.append(content[j]["title"])
                self.author.append(content[j]["alias"])
                self.description.append("默认默认默认默认默认")
                avatarUUID = str(uuid.uuid4())
                self.avatar.append(baseUrl + str(avatarUUID) + ".jpg")
                downloader.download(avatarUUID, 0, content[j]["picuser"])
                previewUUID = str(uuid.uuid4())
                self.preview.append(baseUrl + str(previewUUID) + ".jpg")
                downloader.download(previewUUID, 1, content[j]["picurl"])
                contentUUID = str(uuid.uuid4())
                self.content.append(baseUrl + contentUUID + ".mp4")
                flag3 = downloader.download(contentUUID, 2, content[j]["playurl"])
                if flag3 is True:
                    self.uuid.append(str(uuid.uuid4()))
                else:
                    self.avatar.pop()
                    self.preview.pop()
                    self.title.pop()
                    self.author.pop()
                    self.content.pop()
                    self.description.pop()

    def dataToDataBase(self):
        data = pandas.DataFrame([self.uuid, self.content, self.avatar, self.preview,
                                 self.author, self.description, self.title])
        data = data.T
        print(data)
        host = "121.40.131.167"
        port = 3306
        user = "root"
        pwd = "u8d9*qHmU03@wG%)uiFa"
        databaseName = "tiktok"
        conn_url = f"mysql+pymysql://{user}:{url_parser(pwd)}@{host}:{port}/{databaseName}?charset=utf8mb4"
        engine = create_engine(conn_url)
        data.to_sql("tiktok_local", con=engine, if_exists="append", index=False)
        self.title = []
        self.author = []
        self.uuid = []
        self.avatar = []
        self.content = []
        self.preview = []
        self.description = []


if __name__ == '__main__':
    v = VideoMessageGrabber()
    v.grabVideo(12)
    v.dataToDataBase()
