import pandas as pd
from sqlalchemy import create_engine

# 你的MySQL连接字符串，格式为：mysql+mysql_connector://username:password@host/db
engine = create_engine('mysql+mysql_connector://yourusername:yourpassword@localhost/yourdatabase')

# 一个例子二维矩阵
example_matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 创建Pandas DataFrame
df = pd.DataFrame(example_matrix, columns=['col1', 'col2', 'col3'])

# 将DataFrame导出到MySQL数据库
df.to_sql('matrix_table', con=engine, if_exists='replace', index=False)
