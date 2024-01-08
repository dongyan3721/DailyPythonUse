import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.metrics import classification_report

path = 'ex3data1.mat'
data = scio.loadmat(path)
# 随机选取100个展示
# sample_idx = np.random.choice(np.arange(len(data['X'])), 100)
# sample_image = data['X'][sample_idx, :]
#
# fig, ax_array = plt.subplots(nrows=10, ncols=10, figsize=(12, 12))
# for r in range(10):
#     for c in range(10):
#         ax_array[r, c].matshow(np.array(sample_image[10 * r + c].reshape((20, 20))).T)
#         plt.xticks(np.array([]))
#         plt.yticks(np.array([]))
# plt.show()


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


# 属性
learningRate = 1
input_size = 401
output_size = 10

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
print(type(pred))
print(pred)
print(type(data['X']))
print(classification_report(data['y'], pred))