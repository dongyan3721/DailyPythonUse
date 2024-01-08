"""
多变量线性回归
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def loadDataSet():
    path = 'ex1data2.txt'
    data = pd.read_csv(path, header=None, names=['Size', 'Bedrooms', 'Price'])
    data.head()

    # 正则化
    means = data.mean().values
    stds = data.std().values
    data.describe()
    data = (data - means) / stds
    data.head()

    # 添加b的系数
    data.insert(0, 'Ones', 1)

    cols = data.shape[1]
    X = data.iloc[:, :cols - 1]
    Y = data.iloc[:, cols - 1:cols]

    X = np.matrix(X.values)
    Y = np.matrix(Y.values)
    weights = np.matrix(np.array([0, 0, 0]))
    return X, Y, weights, means, stds


# 定义损失函数
def Cost(X, Y, weights):
    inner = np.power((X * weights.T) - Y, 2)
    return np.sum(inner) / (2 * len(X))


# 梯度下降
def gradientDescent(X, Y, weights, alpha, iters):
    temp = np.matrix(np.zeros(weights.shape))
    parameters = int(weights.shape[1])
    cost = np.zeros(iters)

    for i in range(iters):
        error = X * weights.T - Y

        for j in range(parameters):
            term = np.multiply(error, X[:, j])
            temp[0, j] = temp[0, j] - alpha / len(X) * np.sum(term)

        weights = temp
        cost[i] = Cost(X, Y, weights)

    return weights, cost


# 画出损失图像
def costPlot(cost):
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(np.arange(iters), cost, 'b')
    ax.set_xlabel('iterations')
    ax.set_ylabel('cost')
    ax.set_title('Error correlated with iteration')
    plt.show()


# 回调参数
def weights_transform(weights, means, stds):
    temp = means[:-1] * weights[1:] / stds[:-1]
    weights[0] = (weights[0] - np.sum(temp)) * stds[-1] + means[-1]
    weights[1:] = weights[1:] * stds[-1] / stds[:-1]
    return weights.reshape(1, -1)


if __name__ == '__main__':
    X, Y, weights, means, stds = loadDataSet()
    # perform linear regression on the data set
    alpha = 0.01
    iters = 1000
    g, cost = gradientDescent(X, Y, weights, alpha, iters)
    gT = np.array(g.reshape(-1, 1))
    means = means.reshape(-1, 1)
    stds = stds.reshape(-1, 1)
    weight = weights_transform(gT, means, stds)
    print(weight)
    costPlot(cost)
