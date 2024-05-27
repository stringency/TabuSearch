"""
    城市信息
"""
import numpy as np


class City(object):
    # 城市坐标
    # X = np.array([[16.47, 96.10],
    #               [16.47, 94.44],
    #               [20.09, 92.54],
    #               [22.39, 93.37],
    #               [25.23, 97.24],
    #               [22.00, 96.05],
    #               [20.47, 97.02],
    #               [17.20, 96.29],
    #               [16.30, 97.38],
    #               [14.05, 98.12],
    #               [16.53, 97.38],
    #               [21.52, 95.59],
    #               [19.41, 97.13],
    #               [20.09, 92.55]])
    # test
    X = np.array([[0,1],
                  [1,2],
                  [10,2],
                  [5,4]])
    # 两两城市距离
    # test
    D = np.array([
        [0, 1, 0.5, 1],
        [1, 0, 1, 1],
        [1.5, 5, 0, 1],
        [1, 1, 1, 0]
    ])
    citySize = None
    # 指定起步城市
    beginCity = None

    def __init__(self, X=None, beginCity=0,testflag=0):
        if testflag == 0:
            if X is not None:
                self.X = X
        self.citySize = self.X.shape[0]
        if testflag == 0:
            self.Distance()
        self.beginCity = beginCity

    """
        求两两城市的距离
    """

    def Distance(self):
        self.D = np.zeros([self.citySize, self.citySize])
        self.D.fill(float('inf'))
        for i in range(0, self.citySize):
            for j in range(0, self.citySize):
                if i == j:
                    continue
                self.D[i][j] = self.D[j][i] = np.around(
                    np.sqrt((self.X[i][0] - self.X[j][0]) ** 2 + (self.X[i][1] - self.X[j][1]) ** 2), 3)
