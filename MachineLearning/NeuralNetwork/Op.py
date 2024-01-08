import numpy as np
import scipy.io as scio


class NeuralNetwork():
    def __init__(self):
        # 输入维度
        self.input_size = 400
        # 隐藏神经元维度
        self.hidden_size = 25
        # 输出维度
        self.output_size = 1
        # 学习率
        self.eta = 0.01

        self.weights_ih = np.random.randn(self.input_size, self.hidden_size) * 0.1
        self.bias_ih = np.zeros((1, self.hidden_size))
        self.weights_ho = np.random.randn(self.hidden_size, self.output_size) * 0.1
        self.bias_ho = np.zeros((1, self.output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x.T * (1 - x)

    # 预测
    def feedForward(self, X):
        self.hidden = self.sigmoid(np.dot(X, self.weights_ih) + self.bias_ih)
        self.output = self.sigmoid(np.dot(self.hidden, self.weights_ho) + self.bias_ho)

    # 训练
    def backPropagation(self, X, y):
        # 求梯度
        output_error = y - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)

        hidden_error = np.dot(output_delta, self.weights_ho.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden)

        # 梯度上升更新
        self.weights_ho += np.dot(self.hidden.T, output_delta) * self.eta
        self.bias_ho += np.sum(output_delta, axis=0) * self.eta
        self.weights_ih += np.dot(X.T, hidden_delta) * self.eta
        self.bias_ih += np.sum(hidden_delta, axis=0) * self.eta

    def train(self, X, y):
        self.feedForward(X)
        self.backPropagation(X, y)


if __name__ == '__main__':
    data_path = "ex4data1.mat"

    data = scio.loadmat(data_path)

    dataMat = data['X']
    labelMat = data['y']

    dataMat = np.matrix(dataMat)
    labelMat = np.matrix(labelMat)

    n = NeuralNetwork()
    for i in range(len(dataMat)):
        n.train(dataMat[i], labelMat[i])

    '''
    若有机会做准确性测试最好
    '''
    '''
    data_path_T = "ex4data_test.mat"

    data_T = scio.loadmat(data_path_T)

    dataMat_T = data['X']
    labelMat_T = data['y']

    dataMat_T = np.matrix(dataMat_T)
    labelMat_T = np.matrix(labelMat_T)
    correct = 0
    total = len(dataMat_T)
    for i in range(total):
        n.feedForward(dataMat_T[i])
        if np.argmax(labelMat_T[i]) == np.argmax(n.output):
            correct += 1

    print("Accuracy: ", correct/total)
    '''
