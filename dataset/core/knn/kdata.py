import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier

# 生成数据集
X, y = make_blobs(n_samples=300, centers=3, random_state=42)

# 定义knn可视化函数
def knn_visualization(X, y, k):
    # 训练模型
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, y)

    # 可视化
    plt.figure(figsize=(8, 6))
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Accent, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Set1)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("KNN (k = %i)" % (k))
    plt.show()

# 调用knn可视化函数
knn_visualization(X, y, 1)
knn_visualization(X, y, 5)
knn_visualization(X, y, 10)