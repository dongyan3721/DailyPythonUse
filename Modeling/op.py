import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import classification_report


# sigmoid函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 损失函数
def cost(theta, X, Y, learningRate):
    theta = np.matrix(theta)
    X = np.matrix(X)
    Y = np.matrix(Y)
    first = np.multiply(-Y, np.log(sigmoid(np.dot(X, theta.T))))
    second = np.multiply((1 - Y), np.log(1 - sigmoid(np.dot(X, theta.T))))
    reg = (learningRate / (2 * len(X))) * np.sum(np.power(theta[:, 1:theta.shape[1]], 2))
    return np.sum(first - second) / len(X) + reg


# 梯度下降
def gradient(theta, X, Y, learningRate):
    theta = np.matrix(theta).T
    h = sigmoid(np.dot(X, theta))
    error = h - Y
    grad = (np.dot(X.T, error) / len(X)) + ((learningRate / len(X)) * theta)
    grad[0, 0] = np.dot(X[:, 0].T, error) / len(X)
    return np.array(grad).ravel()


if __name__ == '__main__':
    path = 'dt.xlsx'
    data_r = pd.read_excel(path)
    length = len(data_r)
    data = {}
    data_r = data_r.T
    XX = []
    yy = []
    for i in range(length):
        l1 = []
        for u in list(data_r[i])[8:-1]:
            l1.append(float(u))
        XX.append(l1)
        yy.append(float(list(data_r[i])[-1]))

    data['X'] = np.array(XX)
    data['y'] = np.array(yy)

    # 属性
    learningRate = 1
    input_size = 22
    output_size = 5

    # 初始化x和y
    x = np.insert(data['X'], 0, np.ones(data['X'].shape[0]), axis=1)
    # 参数
    res = np.zeros((input_size, output_size))
    # 多分类拟合过程
    for i in range(1, output_size + 1):
        y = [1 if data['y'][j] == i else 0 for j in range(len(data['y']))]
        y = np.matrix(y).T
        theta = np.zeros(input_size)
        print(cost(theta, x, y, learningRate))
        fmin = minimize(fun=cost, x0=theta, args=(x, y, learningRate), method='TNC', jac=gradient)
        print(cost(fmin.x, x, y, learningRate))
        res[:, i - 1] = fmin.x

    print(res)
    print(res.shape)

    num_labels = res.shape[0]
    h = sigmoid(np.dot(x, res))
    pred = np.argmax(h, axis=1)
    pred = pred + 1
    print(pred)
    print(classification_report(data['y'], pred))

    res_a = np.abs(res)
    res_aa = np.sum(res_a, axis=1) / 5
    items = ["有无任职", "政治面貌", "绩点高低", "挂科数目", "党员学习态度", "学生干部\n学习态度", "自评学习态度", "自修情况", "教师的\n敬业精神", "教师的\n授课水平", "教师的\n学术水平", "教师激发学\n生学习能力",
             "教师在介绍\n新知识方面", "考前复习时间", "对待考试态度", "对考试\n作弊态度", "有无侥幸\n作弊行为", "对所学专业\n感兴趣程度", "学习规划", "学业压力", "与老师沟通"]
    dt = {}
    for i in range(input_size-1):
        dt[items[i]] = res_aa[i+1]

    sorted_dt = dict(sorted(dt.items(), key=lambda xx: xx[1], reverse=True))

    x_value = list(sorted_dt.keys())
    y_value = list(sorted_dt.values())

    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    plt.figure(figsize=(16, 9))
    for i in range(len(x_value)):
        plt.bar(x_value[i], y_value[i])

    plt.title("各影响因素平均权重")
    plt.xlabel("各项影响因素")
    plt.ylabel("平均权重")
    plt.xticks(rotation=90)
    plt.show()
