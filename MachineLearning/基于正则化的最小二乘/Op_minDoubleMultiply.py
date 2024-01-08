import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.optimize import minimize


# 定义正则化线性回归代价的偏导数
def reg_gradient(theta, X, y, Lambda):
    error = X @ theta - y.flatten()
    first_part = X.T @ error / len(X)
    reg = (Lambda / len(X)) * theta
    reg[0] = 0
    return first_part + reg


# 定义正则化线性回归代价函数
def reg_cost(theta, X, y, Lambda):
    error = X @ theta - y.flatten()
    first_part = 1 / (2 * len(X)) * np.sum(np.power(error, 2))
    reg = Lambda / (2 * len(X)) * np.sum(np.power(theta[1:], 2))
    return first_part + reg


# 定义训练过程
def train(X, y, Lambda):
    theta = np.ones(X.shape[1])
    res = minimize(fun=reg_cost, x0=theta, args=(X, y, Lambda), method='TNC', jac=reg_gradient)
    return res.x


# 求出训练集误差和交叉验证集误差以绘制学习曲线
def plot_learningcurve(X, y, X_val, y_val, Lambda):
    x = range(1, X.shape[0] + 1)
    traincosts = []  # 训练集误差的数组
    valcosts = []  # 交叉验证集误差的数组
    for i in x:
        theta_s = train(X[:i, :], y[:i, :], Lambda)  # 用训练集算出θ
        trainingcost = reg_cost(theta_s, X[:i, :], y[:i, :], Lambda)
        valcost = reg_cost(theta_s, X_val, y_val, Lambda)  # 用整个交叉验证集计算验证集误差
        traincosts.append(trainingcost)
        valcosts.append(valcost)
    plt.figure(figsize=(16, 9))
    plt.plot(x, traincosts, label='training cost')
    plt.plot(x, valcosts, label='val cost')
    plt.legend()
    plt.xlabel('number of training examples')
    plt.ylabel('error')
    plt.show()


# 画出拟合曲线
def plotBestFittingLine(theta):

    x = np.linspace(-50, 50, 100)
    f = theta[0] + theta[1] * x
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(data['X'], data['y'], label='training data')
    ax.plot(x, f, 'blue')
    ax.set_xlabel('change in water level x')
    ax.set_ylabel('water flowing out of the dam y')
    plt.show()


if __name__ == '__main__':
    data = loadmat('ex5data1.mat')

    # 训练集
    X = data['X']  # (12,1)
    y = data['y']  # (12,1)
    # print(X.shape, y.shape)

    # 交叉验证集
    X_val = data['Xval']  # (21, 1)
    y_val = data['yval']  # (21, 1)
    # print(X_val.shape, y_val.shape)

    # 测试集
    X_test = data['Xtest']  # (21, 1)
    y_test = data['ytest']  # (21, 1)
    # print(X_test.shape, y_test.shape)

    X = np.insert(X, 0, 1, axis=1)  # (12, 2)
    X_val = np.insert(X_val, 0, 1, axis=1)  # (21, 2)
    X_test = np.insert(X_test, 0, 1, axis=1)  # (21, 2)
    # print(X.shape, X_val.shape, X_test.shape)

    # 作图
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(data['X'], data['y'], label='training data')
    ax.set_xlabel('change in water level X')
    ax.set_ylabel('water flowing out of the dam y')
    plt.show()

    theta = train(X, y, Lambda=0)

    plotBestFittingLine(theta)
    Lambda = 0
    plot_learningcurve(X, y, X_val, y_val, Lambda)
