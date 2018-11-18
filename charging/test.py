from charging.figure import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
if __name__ == '__main__':
    fig_s = figure(file_load='C:\\Users\\智慧小甜心\\Desktop\\czh\\distribute.xlsx', file_traffic='C:\\Users\\智慧小甜心\\Desktop\\czh\\traffic.xlsx')
    fig_s.ini_fig()
    point_set_charging = []
    charging1 = point_charging(13,3,5,2)
    charging2 = point_charging(13,5,7,2)
    charging3 = point_charging(12,6,4,1)
    charging4 = point_charging(5,11,8,2)
    charging5 = point_charging(4,12,6,2)
    charging6 = point_charging(4,13,7,2)
    charging7 = point_charging(2,13,6,2)
    charging8 = point_charging(11,9,4,1)
    point_set_charging.append(charging1)
    point_set_charging.append(charging2)
    point_set_charging.append(charging3)
    point_set_charging.append(charging4)
    point_set_charging.append(charging5)
    point_set_charging.append(charging6)
    point_set_charging.append(charging7)
    point_set_charging.append(charging8)
    fig_s.point_set_charging = point_set_charging

    pik = Pik(fig_s.point_set_traffic,fig_s.point_set_charging)
    pik.Pik1()
    tc = time_comsumption(fig_s.point_set_charging)
    tc.CT(fig_s.point_set_traffic,fig_s.point_set_charging,pik.Pik.copy(),pik.tik.copy(),pik.Pkj.copy(),pik.tkj.copy())
    print(tc.Ct)
    print(pik.Pik)
    fig = plt.figure(figsize=(10,5))
