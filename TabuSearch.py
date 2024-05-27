"""
    禁忌搜素法
"""

import numpy as np

import CityAdapVal
import InitWay

class TabuSearch(object):
    citySize = None
    # 存储禁忌对象
    H_val = None

    # 记录每个个体的最优值
    __path_j = None
    __f_j = None

    # 记录每代最优解；当前这一代的初始化路径为上一代的最优解，避免陷入局部最优
    # test
    path_i = np.array([0, 1, 2, 3])
    f_i = None

    # 最优解
    path_s = None
    f_s = None

    # 禁忌期限
    TabooPeriod = None
    # 连续循环次数
    circSize = None

    # 曾经最优对象，通过方法可以访问
    __H_id = np.array([0,0])

    # 出现循环可能性的标记
    __circPasFlag = 0
    # 记录走过的路径
    passPath = None

    # 迭代次数
    iterations = None
    # 记录迭代将要结束的距离
    iterOver = 1

    """
        H_id:用于放入人为初始化禁忌对象,传入一个(n,3)矩阵
    """
    def __init__(self, CT, TabooPeriod = None,H_id = None, testflag = 0):
        self.citySize = CT.citySize
        if TabooPeriod is None:
            self.TabooPeriod = int(CT.citySize * 3 / 4)
        else:
            self.TabooPeriod = TabooPeriod
        self.circSize = np.copy(self.TabooPeriod)
        self.H_val = np.zeros([self.citySize, self.citySize])
        if H_id is not None:
            for item in H_id:
                indexmin = min(item[0],item[1])
                indexmax = max(item[0],item[1])
                self.H_val[indexmin][indexmax] = item[2]
        self.path_j = np.array([])
        self.f_j = np.inf
        if testflag == 0:
            self.path_i = InitWay.GreedInit(CT.D, CT.beginCity)
        self.f_i = CityAdapVal.EucPathSum(CT.D, self.path_i)
        self.path_s = np.copy(self.path_i)
        self.f_s = np.copy(self.f_i)
        # 记录初始走过的路
        self.passPath = list([])
        self.iterations = 0



    # 更新禁忌长度
    def upH_Val(self):
        for i in range(self.citySize):
            for j in range(i+1,self.citySize):
                if self.H_val[i][j]!=0:
                    self.H_val[i][j] -= 1


    # 通过领域求出  两两交换后的最佳f(i)和最佳路径，并且更新禁忌表id
    def NBIteration(self,D, beginCity):
        # 需要改的全局变量标记为global
        # global H_id
        # global H_val
        # global f_i
        self.path_j = np.array([])
        self.f_j = np.inf
        # 标记需要禁忌的对象
        H_r = 0
        H_c = 0
        # 获取邻域的最好适应值和路径，还有要标记的禁忌对象
        for i in range(self.citySize - 1):
            if self.path_i[i] == beginCity:
                continue
            for j in range(i + 1, self.citySize):
                if self.path_i[j] == beginCity:
                    continue
                path_swap = np.copy(self.path_i)
                indexmin = min(path_swap[i], path_swap[j])
                indexmax = max(path_swap[i], path_swap[j])
                # if H_id.get(indexmin)!=None:
                #     if H_id.get(indexmin)==indexmax:
                #         continue
                if self.H_val[indexmin][indexmax] != 0:
                    continue
                # print("交换前的路径：")
                # print(path_swap)
                path_swap[i], path_swap[j] = path_swap[j], path_swap[i]
                # print("交换后的路径：")
                # print(path_swap)
                """# 记录已经走过的路
                isadd = 1
                for item in self.passPath:
                    if (item == path_swap).all():
                        isadd = 0
                        break
                if isadd == 1:
                    self.passPath.append(path_swap)"""
                # 遇到当代中最优的要进行操作和记录
                if CityAdapVal.EucPathSum(D, path_swap) < self.f_j:
                    self.path_j = np.copy(path_swap)
                    self.f_j = CityAdapVal.EucPathSum(D, path_swap)
                    H_r = min(path_swap[i], path_swap[j])
                    H_c = max(path_swap[i], path_swap[j])
                    # print("相比之前有最好的交换后的路径：")
                    # print(self.path_j)
                    # print("相比之前有最好的交换后的路径适应值：")
                    # print(self.f_j)
                    # print("待定禁忌对象1：")
                    # print(H_r)
                    # print("待定禁忌对象2：")
                    # print(H_c)
        # 记录当代最优适应度
        self.f_i = np.copy(self.f_j)
        self.path_i = np.copy(self.path_j)
        # 先更新禁忌长度
        self.upH_Val()
        # 设置禁忌期限
        self.H_val[H_r][H_c] = self.TabooPeriod
        # 更新最优值
        if self.f_i < self.f_s:
            self.path_s = np.copy(self.path_i)
            self.f_s = np.copy(self.f_i)
            # 更新曾经最优对象
            self.__H_id[0] = H_r
            self.__H_id[1] = H_c
            return 1
        return 0



    # 打印禁忌对象
    def displayTabooObj(self):
        H_id = list()
        for i in range(self.citySize):
            for j in range(i + 1, self.citySize):
                    if self.H_val[i][j] != 0:
                        H_id.append([i,j])
        return H_id


    # 渴望准则
    # 在全部对象都被禁忌后，解禁之前性能最好的对象
    def AspirationCriteria(self):
        # 禁忌对象个数
        TabooObjSize = sum(sum(self.H_val != 0))
        if TabooObjSize == self.citySize - 1:
            self.H_val[self.__H_id[0]][self.__H_id[1]] = 0
            return self.__H_id

    # 判读是要结束,出现曾经走过的路后,再执行禁忌期限(__TabooPeriod)次数循环便退出,若出现了没有走过的路径则置零重新循环
    def overTebuSearch(self):
        for listnum in self.passPath:
            if (listnum == self.path_i).all():
                self.__circPasFlag  = 1
                self.iterOver += 1
                return self.iterOver - 1
        # 加入到已走过路径
        self.passPath.append(self.path_i)
        self.__circPasFlag = 0
        self.iterOver = 1
        return self.iterOver