import pandas as pd

rantings = pd.read_csv("ratings.csv")

movieIds = list(rantings["movieId"])
rating = list(rantings['rating'])
plainDict = {}

for i in range(len(movieIds)):
    if plainDict.keys().__contains__(movieIds[i]) is False:
        plainDict[movieIds[i]] = [rating[i]]
    else:
        plainDict[movieIds[i]].append(rating[i])

index = plainDict.keys()
value = []

for i in index:
    value.append(plainDict[i])

data = pd.DataFrame(value)
data.index = index
# print(len(list(index)))
# print(data.index)
data.to_csv("ratings_n.csv")
