import numpy as np
"充电行为耗时成本"
class time_comsumption():
    def __init__(self,point_set_charging):
        self.Wgq = 0 #充电站平均排队时间
        self.Vi = 0
        self.Ct = 0
        self.q = 20 #驾驶员单位时间成本rmb/h
        self.P = 120 #kW充电机功率
        self.Wevrat = 60# kWh容量
        self.Et = 45 #期望 minute
        self.Vt = 100 #方差
        self.lambda_k = 0 #充电站k的服务参数 时间/辆 平均到达率
        self.c = [point.N_CD for point in point_set_charging] #传入数组 表示充电站k的充电桩个数
        self.Ct = 0

    def CT(self,point_set_traffic,point_set_charging,Pik,tik,Pkj,tkj):

        self.Vi = np.array([point.car_num*0.2 for point in point_set_traffic])#每个交通节点需要充电的车辆数量（取总数20%）

        Qk_taxi = (self.Vi.reshape(-1,1)*Pik).sum(axis=0)#行向量 代表到充电站的车辆总数

        self.lambda_k = Qk_taxi/(4*60) #服务时段4小时 行向量 辆/分钟
        Wgq = np.zeros(len(point_set_charging)) #充电站k等待时间
        for k in range(len(Wgq)):
            cum = 0
            for s in range(self.c[k]):
                cum = cum + np.math.factorial(self.c[k] - 1) * (self.c[k] - self.lambda_k[k] * self.Et) / (
                            np.math.factorial(s) * (self.lambda_k[k] * self.Et) ** (self.c[k] - s))
            Wgq[k] = ((self.Vt + self.Et ** 2) /( 2 * self.Et * (self.c[k] - self.lambda_k[k] * self.Et))) * (1 + cum)**-1
            #为啥是负数？ 排队论待考证
            #Wgq 单位：min
        self.Wgq = Wgq/60 #转为小时
        Vi_P = Pik*self.Vi.reshape(-1,1)  #乘以每个路口的充电需求量 Vi_P为i到达k充电站的出租车数量  矩阵i*k

        cum_VPt = (Vi_P*tik).sum() #Ct的第一个部分 #表示规划区需要充电从出发点到充电站总耗时

        cum_VPW = ((Vi_P.sum(axis=0))*self.Wgq).sum()#Ct 的第二个部分 充电等待时间 2018/11/14

        cum_VPPt = (Vi_P.sum(axis=0)*(Pkj*tkj).sum(axis = 1)).sum()#第三个部分

        self.Ct = 2*self.q*(cum_VPt+cum_VPW+cum_VPPt)*365
"充电站运维费用"
class charging_bo_comsuption():
    def __init__(self,N,charging_set):
        self.N = N #充电站总数
        self.m = 1 #元 单位电价
        self.Nk_charging_device = 0 #充电站k的充电机数量
        self.a = 20000 #变压器单价 元
        self.b = 100000 #充电机单价 元
        self.sk = 0 #充电站基建费用
        self.kt = 0.9#同时率
        self.Tav = 5 #每个充电站集中充电时间段的平均有效时长
        self.r0 = 0.1 #贴现率
        self.z = 30 #运行年限
        self.charging_set = charging_set #充电站集合
        self.CCS = 0 #计算运维费用
        self.ita = 0.1#运维成本比例因子
        self.CVH = 0
        self.CPS = 0


        "年建设成本"
    def CCS(self):

        for charging_station in self.charging_set:
            self.CCS = self.CCS + charging_station.N_CD*self.b+self.sk+self.a*charging_station.N_T
        self.CCS = self.CCS*((self.r0*(1+self.r0)**self.z)/(((1+self.r0)**self.z)-1))

    "年运行维护成本"
    def CVH(self):

        for charging_station in self.charging_set:
            self.CVH = self.CVH +  charging_station.N_CD*self.b+self.sk+self.a*charging_station.N_T
        self.CVH = self.CVH*self.ita


    "充电站的网损年费用"
    def CPS(self):

        for charging_station in self.charging_set:
            # self.CPS =
            self.CPS = self.CPS+charging_station.N_T*(charging_station.C_Fe+charging_station.C_Cu)+charging_station.N_CD*(charging_station.C_L+charging_station.C_D)
        self.CPS = self.CPS*2*365*self.m*self.kt*self.Tav


