import pandas as pd

data = pd.read_excel("ttt.xlsx")
l1 = list(data["学号1"])
l2 = list(data["姓名1"])
l3 = list(data["学号2"])
l4 = list(data["姓名2"])

for i in range(int(len(l1)/4)):
    for j in range(4):
        print(f'{l2[i*4+j]}（{int(l1[i*4+j])}）', end="  ")
    print()

print()
print()

for i in range(int(len(l3) / 4)):
    for j in range(4):
        print(f'{l4[i * 4 + j]}（{int(l3[i * 4 + j])}）', end="  ")
    print()
