from charging.constrains import *
from charging.posibility import *
from charging.opt_function import *
import pandas as pd
import matplotlib.pyplot as plt
class figure():
    def __init__(self,file_load,file_traffic):
        self.file_traffic = file_traffic
        self.file_load = file_load
        self.point_set_load = []
        self.point_set_traffic = []
        self.point_set_charging = []
    def ini_fig(self):

        data_load = pd.read_excel(self.file_load)#电力负荷
        for i in range(len(data_load)):
            p = point_load(data_load['X'][i],data_load['Y'][i],data_load['load'][i])
            self.point_set_load.append(p)
        data_traffic = pd.read_excel(self.file_traffic)#车流信息
        for i in range(len(data_traffic)):
            p = s=point_traffic(data_traffic['X'][i],data_traffic['Y'][i],data_traffic['taxi_num'][i],data_traffic['taxi_demand'][i])
            self.point_set_traffic.append(p)
        fig = plt.figure(figsize=(10,5))

        for point in self.point_set_load:
            plt.scatter(point.X,point.Y,marker='+',c='r')
        for point in self.point_set_traffic:
            plt.scatter(point.X,point.Y,marker='*',c='b')

        plt.show()


if __name__ == '__main__':
    fig = figure(file_load='C:\\Users\\admin\\PycharmProjects\\czh\\distribute.xlsx', file_traffic='C:\\Users\\admin\\PycharmProjects\\czh\\traffic.xlsx')
    fig.ini_fig()