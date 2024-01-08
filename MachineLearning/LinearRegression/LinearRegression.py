"""
单变量线性回归
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# 数据准备
def loadDataSet():
    path = 'ex1data1.txt'
    data = pd.read_csv(path, header=None, names=['Population', 'Profit'])
    # 补足b的系数项
    data.insert(0, 'One', 1)
    column = data.shape[1]
    X = data.iloc[:, 0:column - 1]
    Y = data.iloc[:, column - 1:column]
    X = np.matrix(X.values)
    Y = np.matrix(Y.values)
    weight = np.matrix(np.array([0, 0]))
    return data, X, Y, weight


# 定义计算损失的函数
def computerLost(X, Y, weight):
    tem = np.power((X * weight.T) - Y, 2)
    return np.sum(tem) / (2 * len(X))


# 定义梯度下降函数
def gradientDescent(X, Y, weight, alpha, iters):
    # 存储每一次迭代的损失值方便后续画图直观看
    cost = np.zeros(iters)
    temp = np.matrix(np.zeros(weight.shape))
    parameters = int(weight.shape[1])

    for i in range(iters):
        error = X * weight.T - Y
        for j in range(parameters):
            term = np.multiply(error, X[:, j])
            # 执行梯度下降
            temp[0, j] = temp[0, j] - alpha * np.sum(term) / len(X)
        weight = temp
        cost[i] = computerLost(X, Y, weight)
    return weight, cost


# 画线性最优化函数
def bestFitLinePlot(data, weight):
    x = np.arange(4, 25, 0.1)
    y = weight[0, 0] + weight[0, 1] * x
    plt.figure(figsize=(16, 9))
    plt.xlabel('Population')
    plt.ylabel('Profit')
    plt.plot(x, y, label='Prediction', color='red')
    plt.scatter(data.Population, data.Profit, label='Training Set', )
    plt.legend(loc='best')
    plt.title('Population correlated with Profit')
    plt.show()


# 画出迭代次数和损失函数图像
def plotCost(cost):
    plt.figure(figsize=(16, 9))
    plt.xlabel('iteration')
    plt.ylabel('loss')
    plt.title('loss correlated with iteration')
    plt.plot(np.arange(iters), cost, 'r')
    plt.show()


if __name__ == '__main__':
    data, X, Y, weight = loadDataSet()
    alpha = 0.01
    iters = 1500
    weight, cost = gradientDescent(X, Y, weight, alpha, iters)
    bestFitLinePlot(data, weight)
    plotCost(cost)

