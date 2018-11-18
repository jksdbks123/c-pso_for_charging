import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from charging.part_test import *
from charging.figure import *
class particle():
    def __init__(self,dim):
        self.p = np.zeros(dim)
        self.v = np.zeros(dim)
        self.bp = np.zeros(dim)
        self.fitness = 0
        self.best_fitness = -float('inf')

class PSO():
    def __init__(self,dim,N,limit=[0,16],w = 0.5,c1 = 1.499,c2 = 1.499,v_max = 0.5,iter_max = 1000):
        self.limit = limit
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max
        self.iter_max = iter_max
        self.pop = []
        self.dim = dim
        self.N = N
        self.gp = np.zeros(dim)
        self.group_fitness = -float('inf')

    def z(self,x,y):
        return 3*(1-x)**2*(np.exp(-x**2-(y+1)**2))-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)

    def fitness_func(self,x):
        # return x[0]+10*np.sin(5*x[0])+7*np.cos(4*x[0])
        # x[0] = x
        # x[1] = y
        M = 1e12
        fig_s = figure(file_load='E:\\distribute.xlsx', file_traffic='E:\\traffic.xlsx')
        fig_s.ini_fig()
        point_set_charging = []
        for i in range(5):
            charging_station = point_charging(x[i],x[i+5],0,0)
            point_set_charging.append(charging_station)
        fig_s.point_set_charging = point_set_charging

        pik = Pik(fig_s.point_set_traffic, fig_s.point_set_charging)
        pik.Pik1()
        tc = time_comsumption(fig_s.point_set_charging)
        tc.CT(fig_s.point_set_traffic, fig_s.point_set_charging, pik.Pik.copy(), pik.tik.copy(), pik.Pkj.copy(),
              pik.tkj.copy())

        # result = -a
        "罚函数"
        # for i in range(len(point_set_charging)):
        #
        #     temp = [item for item in point_set_charging if item!= point_set_charging[i]]
        #     dis = []
        #     for item in temp:
        #         dis.append(np.sqrt((point_set_charging[i].X**2-item.X**2)+point_set_charging[i].Y**2-item.Y**2))
        #     dis = np.array(dis)
        #     if False in (dis<3):
        #         result = -a+M #惩罚因子

        return -tc.Ct

        # return  3*(1-x)**2*(np.exp(-x**2-(y+1)**2))-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)

    def find_best(self):
        for bird in self.pop:
            if bird.fitness>self.group_fitness:
                self.group_fitness = bird.fitness
                self.gp = bird.p

    def init_chrom(self):
        for i in range(self.N):
            bird = particle(self.dim)
            for i in range(self.dim):#随机初始化位置
                bird.p[i] = np.random.uniform(self.limit[0],self.limit[1])
                bird.v[i] = -self.v_max+self.v_max*np.random.rand()
            bird.bp = bird.p
            bird.fitness = self.fitness_func(bird.p)
            bird.best_fitness = bird.fitness

            self.pop.append(bird)
        print('initial done!')
        # for i in range(self.N):
        #     bird = particle(self.dim)
        #     for i in range(self.dim):  # 随机初始化位置
        #         bird.p[i] = random_point()
        #         bird.v[i] = -self.v_max+self.v_max*np.random.rand()
        #     bird.bp = bird.p
        #     bird.fitness = self.fitness_func(bird.p)
        #     bird.best_fitness = bird.fitness
        #     self.pop.append(bird)
        # self.find_best()

        "fitness func need"

    def evolution(self):
        for bird in self.pop:
            bird.v = self.w*bird.v+self.c1*np.random.rand()*(bird.bp-bird.p)+self.c2*np.random.rand()*(self.gp-bird.p)
            bird.p = bird.p + bird.v
            for i in range(self.dim):#限制
                if bird.v[i]>self.v_max:
                    bird.v[i] = self.v_max
                if bird.v[i]<-self.v_max:
                    bird.v[i]=-self.v_max
                if bird.p[i] > self.limit[1]:
                    bird.p[i] = self.limit[1]
                if bird.p[i] < self.limit[0]:
                    bird.p[i] = self.limit[0]
            bird.fitness = self.fitness_func(bird.p)
            if bird.fitness > bird.best_fitness:
                bird.best_fitness = bird.fitness
                bird.bp = bird.p

        self.find_best()
        print('evolution time')
    def implement(self):
        fig = plt.figure(figsize=(10,5))
        if self.dim==1:
            plt.figure(figsize=(10, 5))
            plt.plot(np.linspace(-10, 10, 1000), self.fitness_func([np.linspace(-10, 10, 1000)]))
            for i in range(self.iter_max):
                plt.scatter(self.gp, self.fitness_func(self.gp), marker='+', s=500)
                self.evolution()
                print('群最佳位置:',self.gp,'群最佳适应度:',self.group_fitness)
            plt.show()
        else:
            # ax = Axes3D(fig)
            # X = np.linspace(-3, 3, 100)
            # Y = np.linspace(-3, 3, 100)
            # X, Y = np.meshgrid(X, Y)
            # Z = self.z(X, Y)
            # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow',alpha = 0.5)
            # X1 = []
            # Y1 = []
            # Z1 = []
            # for i in range(self.iter_max):
            #     self.evolution()
            #     print(i)
            #     print(self.group_fitness, self.gp)
            j = 1
            while(True):

                self.evolution()
                print(j)
                point = []
                for i in range(len(self.gp)-5):
                    print(self.gp[i],self.gp[i+5])
                print(-self.group_fitness)
                j += 1




if __name__ == '__main__':


    pso = PSO(dim=10,N=20,iter_max=100)
    pso.init_chrom()
    pso.implement()







