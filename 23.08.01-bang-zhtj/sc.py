import json

import _jpype
import jpype
import requests
from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader as PlainJsonReader


class Encryptor:
    def __init__(self, publicKey, javaPackageName, relativeClassAddress):
        self.publicKey = publicKey
        JVMPath = jpype.getDefaultJVMPath()
        jpype.startJVM(JVMPath, "-ea", "-Djava.class.path=" + javaPackageName)
        self.RSAEncryptor = jpype.JClass(relativeClassAddress)

    def RSAEncryption(self, plaintext):
        rSAEncryptor = self.RSAEncryptor()
        encryptionText = rSAEncryptor.encryptRSA(plaintext, self.publicKey)
        return encryptionText

    def releaseResource(self):
        self.RSAEncryptor = None
        jpype.shutdownJVM()


class CaptchaDownloader:
    def __init__(self, url: str, session: requests.Session):
        self.url = url
        self.session = session

    def parse(self, jsonReader: PlainJsonReader):
        content = session.get(url=self.url, headers=jsonReader.read("captcha_image_headers")).content
        with open(jsonReader.read("local_captcha_name"), "wb+") as f:
            f.write(content)
            f.close()


if __name__ == "__main__":
    # Original data
    reader = PlainJsonReader("application.json")

    account = reader.read("account")
    password = reader.read("password")

    public_key = reader.read("public_key")
    encryptor = Encryptor(publicKey=public_key, javaPackageName=reader.read("java_package_name"),
                          relativeClassAddress=reader.read("relative_class_address"))

    retCode = -1015
    session = requests.Session()
    while retCode != 1000:
        encrypted_acc = str(encryptor.RSAEncryption(account))
        encrypted_pwd = str(encryptor.RSAEncryption(password))

        captcha_id = session.get(url=reader.read("captcha_interface_url"),
                                 headers=reader.read("captcha_interface_headers")).json()["results"]["captchaId"]

        print(session.cookies)

        print(captcha_id)

        captcha_image_url = reader.read("base_captcha_image_url") + captcha_id

        downloader = CaptchaDownloader(captcha_image_url, session)
        print(session.cookies)
        downloader.parse(reader)

        captcha_value = input("请输入同目录下{}的值...".format(reader.read("local_captcha_name")))
        data = {
            "captcha": captcha_value,
            "captcha_Id": captcha_id,
            "ident": encrypted_acc,
            "password": encrypted_pwd
        }

        resp = session.post(url=reader.read("login_interface_url"), headers=reader.read("login_interface_headers"),
                            data=data)
        print(session.cookies)
        print(data)
        print(resp.text)
        retCode = int(resp.json()["retCode"])

    encryptor.releaseResource()

    #  grab data with cookie return by surf-casting
    #  try RSA login
