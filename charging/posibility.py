import numpy as np
"从交通节点i出发，选择充电站k接受服务的概率"
class Pik():
    def __init__(self,point_set_traffic,point_set_charging):

        self.theta = 1
        self.alpha1 = 1
        self.alpha2 = 0.5
        self.alpha3 = 0.5
        self.delta = 1
        self.beta1 = 1
        self.beta2 = 0.5
        self.velocity_av = 30 #km/h
        self.Wmax = 10 #充电站排队等待时间约束上限 min
        self.point_set_traffic = point_set_traffic
        self.point_set_charging = point_set_charging
        self.Pik = 0 #交通节点i到充电站k充电的几率
        self.tik = 0#交通节点i到充电站k充电的最短时间（欧几里得距离）
        self.Uik = 0#i到k效用函数
        self.tkj = 0
        self.Pkj = 0

    def Pik1(self):
        tik = np.zeros((len(self.point_set_traffic),len(self.point_set_charging))) #k充电站数量 i交通节点数量
        for i in range(len(self.point_set_traffic)):
            for k in range(len(self.point_set_charging)):
               tik[i][k] = np.sqrt((self.point_set_traffic[i].X - self.point_set_charging[k].X)**2 + (self.point_set_traffic[i].Y - self.point_set_charging[k].Y)**2)*1.2/self.velocity_av#折线系数1.2

        # Uik = self.alpha1 * traffic_range_Set+self.alpha2*self.Wmax+self.alpha3*tk2#tk2

        #  tik 交通节点i到充电站k的最短行驶时间，d/v = t

        tkj = np.zeros((len(self.point_set_charging),len(self.point_set_traffic)))
        for k in range(len(self.point_set_charging)):
            for j in range(len(self.point_set_traffic)):
                tkj[k][j] = np.sqrt((self.point_set_charging[k].X - self.point_set_traffic[j].X)**2 + (self.point_set_charging[k].Y - self.point_set_traffic[j].Y)**2)*1.2/self.velocity_av
        #  tkj 充电站k到交通节点j的最短行驶时间，d/v = t

        q = []
        for i in range(len(self.point_set_traffic)):
            q.append(self.point_set_traffic[i].demand)
        q = np.array(q)
        Pkj = np.exp(-self.delta*(tkj**self.beta1)*q**(-self.beta2))# 2018/9/25/18:12
        for k in range(len(self.point_set_charging)):
           Pkj[k] = Pkj[k]/Pkj.sum(axis = 1)[k]

        tk2 = (tkj * Pkj).sum(axis = 1)

        Uik = self.alpha1 * tik + self.alpha2 * self.Wmax + self.alpha3*tk2#i*k矩阵

        # Uik = self.alpha1*tik+self.alpha2*self.Wmax+self.alpha3*tk2

        Pik = np.exp(-self.theta*Uik)
        for i in range(len(self.point_set_traffic)):
            Pik[i] = Pik[i]/Pik.sum(axis = 1)[i]
        self.Pik = Pik
        self.tik = tik
        self.Uik = Uik
        self.tkj = tkj
        self.Pkj = Pkj


