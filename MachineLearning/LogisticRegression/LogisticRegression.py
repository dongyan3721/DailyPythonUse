from numpy import *
import matplotlib.pyplot as plt


def loadData(filename):
    dataMat = []
    labelMat = []
    f = open(filename, "r")
    for line in f.readlines():
        lineData = line.strip().split()
        dataMat.append([1.0, float(lineData[0]), float(lineData[1])])
        labelMat.append(int(lineData[2]))

    return dataMat, labelMat


def sigmoid(x):
    return 1.0 / (1 + exp(-x))


def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    alpha = 0.0001
    maxCycles = 5000
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)  # 求梯度并执行梯度上升算法
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


def plotBestFit(weights, filename):
    dataMat, labelMat = loadData(filename)
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='black', marker='x')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = [(-float(weights[0]) - float(weights[1]) * xx) / float(weights[2]) for xx in x]
    ax.plot(x, y)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()


if __name__ == '__main__':
    dataMat, labelMat = loadData("testSet.txt")
    weight = gradAscent(dataMat, labelMat)
    plotBestFit(weight, "testSet.txt")
    plotBestFit(weight, "test.txt")

