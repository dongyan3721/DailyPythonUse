# import requests
# from InternetThemedCommunistLeagueClass.InterfacePraparation import DoubtfulJsonReader
#
#
# # url = "https://vi1.6rooms.com/live/2021/11/09/23/1003v1636470220065845679.jpg"
# import re
# url = "https://vi0.6rooms.com/live/2022/09/21/10/1003v1663728117071766614.jpg"
#
# print(re.findall("\.jpg|mp4", url)[0])
#
# reader = DoubtfulJsonReader("settings.json")
#
# print(requests.get(url=url).text.__contains__("html"))


# import os
# import shutil
#
#
# def copy_and_rename_file(source_dir, target_dir, file_name, new_file_name):
#     if not os.path.exists(target_dir):
#         os.makedirs(target_dir)
#
#     source_file_path = os.path.join(source_dir, file_name)
#     target_file_path = os.path.join(target_dir, new_file_name)
#
#     if os.path.exists(source_file_path):
#         shutil.copy(source_file_path, target_file_path)
#         print(f"File {source_file_path} copied to {target_file_path}")
#     else:
#         print(f"File {file_name} does not exist in {source_dir}.")
#
#
# if __name__ == '__main__':
#     source_directory = '.'  # 修改为你的源目录
#     target_directory = './avatar'  # 修改为你的目标目录
#     file_to_copy = 'fail.png'  # 修改为你要复制的文件名
#     new_file_name = 'success.png'  # 修改为你要命名的新文件名
#
#     copy_and_rename_file(source_directory, target_directory, file_to_copy, new_file_name)


# print("https://localhost:8080/getRes/afbb7bf3-e9b8-4772-81cb-62b4e82e7b52.mp4"[30:])
import random

les = ['301-231235', '321-314342', '738-237823', '892-382188', '900-123123', '901-378230', '928-123564']
st = [
    '2135030210',
    '2135072342',
    '2135042453',
    '2135071931',
    '2135061234',
    '2135054301',
    '2135063142',
    '2135051702'
]

ins = 'insert into '

for i in range(30):
    print(f"insert into lesson_selection(student_ID, lesson_ID) values {st[random.randint(0, len(st)-1)], les[random.randint(0, len(les)-1)]};")
