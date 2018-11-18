from charging.opt_function import *
from charging.points import *
from charging.PSO import *
class testing():
    def __init__(self):
        self.round = [i for i in range(4,12)]
    def imple(self):
        pso = PSO(dim=5, N=20, iter_max=100,limit=[[0,16],[0,16],[0,16],[0,16],[0,16],[0,16],[0,16],[0,16],[0,16],[0,16]]) #5个站的情况
        pso.init_chrom()
        pso.implement()