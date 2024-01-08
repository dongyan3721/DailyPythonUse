# import scipy.io as scio
#
# import pandas as pd
#
# data_path = "ex4weights.mat"
#
# # Method 1
#
# data = scio.loadmat(data_path)

# data_train_label = data.get('label')  # 取出字典里的label
#
# data_train_data = data.get('data')  # 取出字典里的data
# print(data['X'])
# print(len(data['X'][0]))
# print(data['X'][0])
# for i in data['y']:
#     print(i)

# print(len(data['Theta1']))
# print(data['Theta1'][0])
# print(len(data['Theta2'][0]))
print("Accuracy: ", 4984/5000)