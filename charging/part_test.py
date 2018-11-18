from charging.figure import *
def random_point():
    x1, y1 = -6, 16
    x3, y3 = 16, -6
    x2, y2 = 16, 16  # 区域顶点
    sample_size = 5
    theta = np.arange(0, 1, 0.001)
    x = theta * x1 + (1 - theta) * x2
    y = theta * y1 + (1 - theta) * y2
    # plt.plot(x, y, 'g--', linewidth=2)
    x = theta * x1 + (1 - theta) * x3
    y = theta * y1 + (1 - theta) * y3
    # plt.plot(x, y, 'g--', linewidth=2)
    x = theta * x2 + (1 - theta) * x3
    y = theta * y2 + (1 - theta) * y3
    # plt.plot(x, y, 'g--', linewidth=2)
    rnd1 = np.random.random(size=sample_size)
    rnd2 = np.random.random(size=sample_size)
    rnd2 = np.sqrt(rnd2)
    x = rnd2 * (rnd1 * x1 + (1 - rnd1) * x2) + (1 - rnd2) * x3
    y = rnd2 * (rnd1 * y1 + (1 - rnd1) * y2) + (1 - rnd2) * y3
    # plt.plot(x, y, 'ro')
    # plt.grid(True)
    plt.show()
    # print(x,y)
    lis = x.tolist()
    for item in y:
        lis.append(item)
    # print(lis)
    return np.array(lis)
    # point_set_charging = []
    # for i in range(len(x)):
    #     charging_station = point_charging(x[i], y[i], 3, 2)
    #     point_set_charging.append(charging_station)
    # return point_set_charging

def ini_point():
    ita_EV = 0.9
    v_EV = 30
    S_opt = 0.5
    S_max = 0.3
    ita_I = 1.27
    W_rat_EV = 60
    V_EV = 384
    P_EV = 100
    D_E_EV = (ita_EV * v_EV * (S_opt - S_max) * ita_I * W_rat_EV * V_EV) / P_EV  # 最佳行驶距离

    while (True):
        flag = True
        point_set_charging = random_point()
        for i in range(len(point_set_charging)):
            temp = [item for item in point_set_charging if item!= point_set_charging[i]]
            for item in temp:
                dis = np.sqrt((point_set_charging[i].X**2-item.X**2)+point_set_charging[i].Y**2-item.Y**2)
                if (dis<D_E_EV)|(dis>2*D_E_EV):
                    flag = False
                    break
            if flag==False:
                break
        if flag:
            break
    print("范围:",D_E_EV)
    mat = np.zeros((5,5))
    for i in range(len(point_set_charging)):
        for j in range(len(point_set_charging)):
            mat[i][j] = np.sqrt((point_set_charging[i].X**2-point_set_charging[j].X**2)+point_set_charging[i].Y**2-point_set_charging[j].Y**2)
    print(mat)
    # return point_set_charging







if __name__ == '__main__':
    lis = random_point()
    print(lis)






