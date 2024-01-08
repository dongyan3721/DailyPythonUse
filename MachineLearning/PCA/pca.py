import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from scipy.io import loadmat


# def find_closest_centroids(X, centroids):
#     m = X.shape[0]
#     k = centroids.shape[0]
#     idx = np.zeros(m)
#
#     for i in range(m):
#         min_dist = 1000000
#         for j in range(k):
#             dist = np.sum((X[i, :] - centroids[j, :]) ** 2)
#             if dist < min_dist:
#                 min_dist = dist
#                 idx[i] = j
#
#     return idx
#
#
# data = loadmat('data/ex7data2.mat')
# X = data['X']
# initial_centroids = np.array([[3, 3], [6, 2], [8, 5]])
#
# idx = find_closest_centroids(X, initial_centroids)
#
# data2 = pd.DataFrame(data.get('X'), columns=['X1', 'X2'])
# data2.head()
#
# sb.set(context="notebook", style="white")
# sb.lmplot('X1', 'X2', data=data2, fit_reg=False)
# plt.show()
#
#
# def compute_centroids(X, idx, k):
#     m, n = X.shape
#     centroids = np.zeros((k, n))
#
#     for i in range(k):
#         indices = np.where(idx == i)
#         centroids[i, :] = (np.sum(X[indices, :], axis=1) / len(indices[0])).ravel()
#
#     return centroids
#
#
# def run_k_means(X, initial_centroids, max_iters):
#     m, n = X.shape
#     k = initial_centroids.shape[0]
#     idx = np.zeros(m)
#     centroids = initial_centroids
#
#     for i in range(max_iters):
#         idx = find_closest_centroids(X, centroids)
#         centroids = compute_centroids(X, idx, k)
#
#     return idx, centroids
#
#
# cluster1 = X[np.where(idx == 0)[0], :]
# cluster2 = X[np.where(idx == 1)[0], :]
# cluster3 = X[np.where(idx == 2)[0], :]
#
# fig, ax = plt.subplots(figsize=(12, 8))
# ax.scatter(cluster1[:, 0], cluster1[:, 1], s=30, color='r', label='Cluster 1')
# ax.scatter(cluster2[:, 0], cluster2[:, 1], s=30, color='g', label='Cluster 2')
# ax.scatter(cluster3[:, 0], cluster3[:, 1], s=30, color='b', label='Cluster 3')
# ax.legend()
# plt.show()

data = loadmat('data/ex7data1.mat')

X = data['X']

fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(X[:, 0], X[:, 1])
plt.show()

def pca(X):
    # normalize the features
    X = (X - X.mean()) / X.std()

    # compute the covariance matrix
    X = np.matrix(X)
    cov = (X.T * X) / X.shape[0]

    # perform SVD
    U, S, V = np.linalg.svd(cov)

    return U, S, V

U, S, V = pca(X)

# 低维投射
def project_data(X, U, k):
    U_reduced = U[:,:k]
    return np.dot(X, U_reduced)

# 原始数据恢复
def recover_data(Z, U, k):
    U_reduced = U[:,:k]
    return np.dot(Z, U_reduced.T)
Z = project_data(X, U, 1)

X_recovered = recover_data(Z, U, 1)

fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(list(X_recovered[:, 0]), list(X_recovered[:, 1]))
plt.show()
