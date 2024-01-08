import pandas as pd
import mysql.connector
from mysql.connector import Error
from grab import copy_and_rename_file


# 连接到MySQL数据库
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="121.40.131.167",
            user="root",
            password="u8d9*qHmU03@wG%)uiFa",
            database="tiktok"
        )
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(f"Error: {e}")
    return connection


# 从MySQL数据库中读取数据
def read_table_to_dataframe(connection, table_name):
    if connection is not None and connection.is_connected():
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, con=connection)
        return df
    else:
        print("Database connection error.")


def getResourceName(l):
    ret = []
    for i in l:
        ret.append(i[30:])
    return ret


# 读取MySQL表到DataFrame
connection = create_db_connection()
df = read_table_to_dataframe(connection, 'tiktok_local')  # 替换为你的表名
# print(df['0'])

existContent = list(df['1'])
existContent = getResourceName(existContent)
existAvatar = list(df['2'])
existAvatar = getResourceName(existAvatar)
existPreview = list(df['3'])
existPreview = getResourceName(existPreview)

for i in existContent:
    copy_and_rename_file("./content", "./nC", i, i)

for i in existPreview:
    copy_and_rename_file("./preview", "./nP", i, i)

for i in existAvatar:
    copy_and_rename_file("./avatar", "./nA", i, i)

# 关闭数据库连接
if connection.is_connected():
    connection.close()
    print("MySQL database connection is closed")
