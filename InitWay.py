"""
    用贪心算法选取最初始优解
"""

import numpy as np


def GreedInit(D, beginCity) -> np.ndarray:
    len = D.shape[0]
    Dtmp = np.copy(D)  # 复制一个两两城市距离
    path = np.array(np.zeros(len), np.uint64)  # 记录行走城市顺序
    CityIsGo = np.array(np.ones(len), np.uint64)  # 记录已经走过的城市
    # 自定义起始点
    # cusid = 0 # 起步城市
    # 默认从0开始走
    path[0] = beginCity
    CityIsGo[beginCity] = 0
    j = path[0]  # 记录下一个要走的最短路线城市，初始化为下一个索引

    for i in range(1, len):
        pathidtmp = np.argmin(Dtmp[path[i - 1]])  # 要放问的城市编号
        # 找到没有访问过的城市
        while CityIsGo[pathidtmp] == 0:
            Dtmp[path[i - 1]][pathidtmp] = Dtmp[pathidtmp][path[i - 1]] = 'inf'
            pathidtmp = np.argmin(Dtmp[path[i - 1]])  # 找下一个没访问过的最小值
        path[i] = pathidtmp  # 记录走这个城市
        # 已经走过后要标记好，以便后面不再走
        Dtmp[path[i - 1]][path[i]] = Dtmp[path[i]][path[i - 1]] = 'inf'
        CityIsGo[path[i]] = 0
    return path
