import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from charging.part_test import *
class particle():
    def __init__(self,dim):
        self.p = np.zeros(dim)
        self.v = np.zeros(dim)
        self.bp = np.zeros(dim)
        self.fitness = 0
        self.best_fitness = -float('inf')

class PSO():
    def __init__(self,dim,N,limit=[-3,3],w = 0.5,c1 = 1.499,c2 = 1.499,v_max = 1,iter_max = 1000,c = 1.2):
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
        self.c = c
        self.k = 1
        self.P = 0 #惩罚项
        self.epsilon = 10e-4
        self.delta = 1

    def z(self,x,y):
        return 3*(1-x)**2*(np.exp(-x**2-(y+1)**2))-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)
        # return (1/3)*(x+1)**3+y


    def fitness_func(self,x,alpha=2,beta = 2):
        # return x[0]+10*np.sin(5*x[0])+7*np.cos(4*x[0])
        # x[0] = x
        # x[1] = y
        # return -(3 * (1 - x[0]) ** 2 * (np.exp(-x[0] ** 2 - (x[1] + 1) ** 2)) - 10 * (x[0] / 5 - x[0] ** 3 - x[1] ** 5) * np.exp(-x[0] ** 2 - x[1] ** 2) - 1 / 3 * np.exp(-(x[0] + 1) ** 2 - x[1] ** 2))
        # return  3*(1-x)**2*(np.exp(-x**2-(y+1)**2))-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)
        unequation = 0
        if x[1]<0:
            unequation = x[1]
        self.P = self.c*(np.abs(x[0]+x[1]-1)**2 +np.min(x[1],0)+unequation)
        return -(1/3)*(x[0]+1)**3+x[1]+self.delta*self.P#x+y = 1,y>=0

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
        self.find_best()
        self.k = 1
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
        self.k = self.k + 1
        self.delta = self.delta*self.c

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
            ax = Axes3D(fig)
            X = np.linspace(-5, 5, 100)
            Y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(X, Y)
            Z = self.z(X, Y)
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow', alpha=0.5)
            X1 = []
            Y1 = []
            Z1 = []
            self.init_chrom()
            # if self.P>self.epsilon:
            for i in range(self.iter_max):
                print(self.k)
                self.evolution()
                if self.P<self.epsilon:
                    break
                X1.append(self.gp[0])
                Y1.append(self.gp[1])
                Z1.append(-self.group_fitness)
                print(self.group_fitness, self.gp)
            # else:print('P<eps')
            ax.scatter(X1, Y1, Z1, marker="+",s=300,color='black',alpha=1)
            plt.show()



if __name__ == '__main__':


    pso = PSO(dim=2,N=20,iter_max=100)
    pso.implement()







