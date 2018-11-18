class point_load():
    def __init__(self,X,Y,load):
        self.X = X
        self.Y = Y
        self.load = load
class point_traffic():
    def __init__(self,X,Y,car_num,demand):
        self.X = X
        self.Y = Y
        self.car_num = car_num
        self.demand = demand
class point_charging():
    def __init__(self,X,Y,N_CD,N_T):
        self.X = X
        self.Y = Y
        self.N_CD = N_CD #充电机个数
        self.N_T = N_T#变压器个数
        self.C_Fe = 0 #铁损耗
        self.C_Cu = 0 #铜损耗
        self.C_L = 0.05 #充电站内线路损耗折算到每一台充电机的损耗 元/kwh
        self.C_D = 0.05 #单台充电机充电损耗 元/kwh
