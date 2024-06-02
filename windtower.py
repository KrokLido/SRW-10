from trigonometria import sin, cos, asin

# import libf2
import atmosphere_GOST4401_81 as atm
import let_point_thy_path as lptp
import cxyz

# import math


def geometric_calculations(m_payload, mu_0, mu_1, yakor0, yakor1, I10, I11, d, beta=1.4):
    m_sum = m_payload / ((1 - beta * mu_0) * (1 - beta * mu_1))

    m_0 = m_sum * mu_0 * beta
    m_0fuel = m_sum * mu_0

    m_1 = m_sum - m_0 - m_payload
    # m_1fuel = (m_sum - m_0) * mu_1
    m_1fuel = m_1 / beta

    P_10 = yakor0 * m_sum * 9.86
    P_11 = yakor1 * (m_1 + m_payload) * 9.86

    G0 = P_10 / I10
    G1 = P_11 / I11

    F_midelya = 3.14 * d**2 / 4

    ans = {}
    ans["m_sum"] = m_sum
    ans["G_10"] = G0
    ans["G_11"] = G1
    ans["m_payload"] = m_payload
    ans["m_sum"] = m_sum
    ans["m_0"] = m_0
    ans["m_0fuel"] = m_0fuel
    ans["m_1"] = m_1
    ans["m_1fuel"] = m_1fuel
    ans["I_10"] = I10
    ans["I_11"] = I11
    ans["yakor_0"] = yakor0
    ans["yakor_1"] = yakor1
    ans["F_m"] = F_midelya
    ans["P_10"] = P_10
    ans["P_11"] = P_11
    return ans


def system_equations(d, dt=0.01):
    def xyzk(name, ldc, xy):
        if xy == 0:
            return 0
        if xy < 0:
            xy = abs(xy)
        if name == "x":
            lx = []
            ly = []
            lx = ldc[0]["lx"].copy()
            ly = ldc[0]["ly"].copy()
            table = {}
            table["x"] = lx
            table["y"] = ly
            cx = cxyz.get_value(table, xy)
            return cx
        if name == "y":
            lx = []
            ly = []
            lx = ldc[1]["lx"].copy()
            ly = ldc[1]["ly"].copy()
            table = {}
            table["x"] = lx
            table["y"] = ly
            cx = cxyz.get_value(table, xy)
            return cx
        if name == "z":
            lx = []
            ly = []
            lx = ldc[2]["lx"].copy()
            ly = ldc[2]["ly"].copy()
            table = {}
            table["x"] = lx
            table["y"] = ly
            cx = cxyz.get_value(table, xy)
            return cx

    cx = xyzk("x", d["ldc"], d["alpha"])
    # print('cx = ', cx)

    V = (
        d["v"]
        + (
            (1 / d["m"])
            * (
                d["p"]
                - (d["i"] * cx * d["fm"] * d["rho"] * d["v"] ** 2) / 2
                - d["m"] * 9.86 * sin(d["teta"])
            )
        )
        * dt
    )
    # teta = d['n_ya'] * 9.86 * dt / d['v']
    teta = d["teta"]
    x = d["x"] + d["v"] * cos(teta) * dt
    y = d["y"] + d["v"] * sin(teta) * dt

    d["v"] = V
    d["x"] = x
    d["y"] = y
    # d['teta'] = teta


def reteta(
    teta_r,
    xr,
    yr,
    xc,
    yc,
    n,
    vr,
    vc,
    teta_c,
    letter="2_point",
    preteta=0,
    border=10000,
    dt=0.01,
):
    length = (
        lambda xr, yr, xc, yc: ((xr - xc) ** 2 + (yr - yc) ** 2) ** 0.5
    )  # Лямбда-функция нахождения дистанции до цели.

    # print(length(xr, yr, xc, yc))
    direction = lptp.water_teta(
        xc, yc, xr, yr
    )  # Определим угол отрезка, соединяющего точки положеня ракеты и цели.
    direction = min(abs(direction), abs(360 - direction))  # Выбрать минимальный угол.
    # print("direction = ", direction)
    # Предопределение скорости.
    if vr == 0:
        vr = 0.01
    teta_new = 1 * (n * 9.86 / vr) * dt  # Возможный угол поворота ракеты.
    # Метод самонаведения по двум точкам (прямое наведение без угла упреждения)
    if letter == "2_point":
        delta = teta_r - direction  # Разность нужных углов.
        if abs(delta) < abs(teta_new):
            return teta_r - delta
        else:
            if delta < 0:
                return teta_r - teta_new
            else:
                return teta_r + teta_new
    # Метод самонаведения с упреждением по координате полёта цели (исходя из скорости полёта цели)
    elif letter == "2_point_prelength":
        # Упреждение на <preteta> скоростей полёта цели.
        xcf = xc + vc * cos(teta_c) * dt * preteta
        ycf = yc + vc * sin(teta_c) * dt * preteta
        direction = lptp.water_teta(
            xcf, ycf, xr, yr
        )  # Переопределяем нужный угол полёта.
        delta = teta_r - direction
        if abs(delta) < abs(teta_new):
            return teta_r - delta
        else:
            if delta < 0:
                return teta_r - teta_new
            else:
                return teta_r + teta_new
    # Метод самонаведения с упреждением по углу.
    elif letter == "2_point_preteta":
        delta = teta_r - direction
        print("xc = %s, yc = %s, xr = %s, yr = %s" % (xc, yc, xr, yr))
        print(delta, "\t\t", teta_r, "\t\t", teta_new)
        print(length(xr, yr, xc, yc))
        # dphi = (-vc * sin(teta_r - teta_c)) / length(xc, yc, xr, yr)
        if abs(delta) > 10 and vr > 1000:
            print("Это конец, я тут умру и меня отчислят")
            print(length(xr, yr, xc, yc))
            # a = input()
        if yr > 100:

            if delta < 0:
                delta += preteta
            elif delta > 0:
                delta -= preteta
        # print(delta, '\t\t', teta_r, '\t\t', teta_new)
        if abs(delta) < abs(teta_new):
            return teta_r - delta
        else:
            if delta < 0:
                return teta_r - teta_new
            else:
                return teta_r + teta_new
    # Метод параллельного сближения.
    elif letter == "parallel":
        # Контроль скорости ракеты.
        if (vc) / vr * sin(direction - teta_c) > 1:
            vr = (
                sin(direction - teta_c) / vc
            ) ** -1 + 0.5  # Т.е. вычисляем минимальную скорость ракеты, чтобы аргумент арксинуса существовал в пределах [-1;1] и добавляем 0.5м/с, чтобы точно было больше границы.
        # print(asin((vc)/(vr) * sin(direction - teta_c)))
        # print((vc)/(vr) * sin(direction - teta_c))
        teta = direction - asin((vc) / (vr) * sin(direction - teta_c))
        return teta


def main_system(d, dt=0.01):
    def inf_dreturn(lrx, lry, l_t, lvr, lm, answer, flag, lcx, lcy):
        ret = {}
        ret["l_x"] = lrx.copy()
        ret["l_y"] = lry.copy()
        ret["lcx"] = lcx.copy()
        ret["lcy"] = lcy.copy()
        ret["flag"] = flag
        ret["l_V_sum"] = lvr.copy()
        ret["l_m"] = lm.copy()
        ret["l_t"] = l_t.copy()
        ret["answer"] = answer
        return ret

    def inf_answer(position, retflag=False):
        if position == "start":
            if retflag:
                return True
            return "Ракета достигла своей цели на стартовом участке."
        if position == "march":
            if retflag:
                return True
            return "Ракета достигла своей цели на маршевом участке."
        if position == "fatigue":
            if retflag:
                return True
            return "Ракета достигла своей цели на пассивном участке."
        if position == "fall":
            if retflag:
                return False
            return "Ракета не долетела."
        if position == "M<V":
            if retflag:
                return False
            return "Ракета не набрала нужной скорости."
        if position == "atmosphere":
            if retflag:
                return False
            return "Ракета вылетела за пределы атмосферы."
        if position == "n":
            if retflag:
                return False
            return "Ракета не может осуществить поворот с требуемой перегрузкой."
        if position == "missing":
            if retflag:
                return False
            return "Ракета промахнулась."
        else:
            if retflag:
                return False
            return "Здесь был бред"

    # Функция расчёта дальности до цели.
    def L_to_point(x, y, xp, yp):
        xt = abs(xp - x)
        yt = abs(yp - y)
        L = (xt**2 + yt**2) ** 0.5
        return L

    # Нужны: данные по ракете, координаты цели[xc, yc]
    # Подготовка
    lrx = []
    lry = []
    lcx = []
    lcy = []

    xc = d["xc"]
    yc = d["yc"]
    vc = d["vc"]
    tetac = d["tetac"]
    t = 0

    lrv = []
    # lcv = []

    lrm = []
    lt = []
    dra = atm.get_table(fcsv=True)
    altmax = atm.getmax() - 1000
    # print("ALTMAX = ", altmax)
    dcx = {}
    # dcy = {}
    dcx["lx"], dcx["ly"] = cxyz.get_table("cx")
    ldc = []
    ldc.append(dcx)
    d["ldc"] = ldc.copy()

    if "direction_law" not in d:
        # print("У МЕНЯ НЕТУ ТАКИХ КЛЮЧЕЙ!!!!!")
        direction_law = "2_point"
        direction_law_preteta = 0
        # print("direction_law = %s, direction_law_preteta = %s" %(direction_law, direction_law_preteta))
    else:
        direction_law = d["direction_law"]
        direction_law_preteta = d["direction_law_preteta"]

    # mfuel_0 = d["m_0fuel"]
    # mfuel_1 = d["m_1fuel"]

    dbell = {}
    dbell["v"] = d["v_start"]
    dbell["teta"] = d["teta_0"]
    dbell["x"] = d["xr0"]
    dbell["y"] = d["yr0"]
    dbell["n_ya"] = 0
    dbell["m"] = d["m_sum"]
    dbell["p"] = d["P_10"]
    dbell["i"] = d["i"]
    dbell["fm"] = d["F_m"]
    dbell["ldc"] = ldc.copy()
    dbell["alpha"] = d["alpha"]
    dbell["rho"] = atm.f_rho_dra(dbell["y"], dra)

    # Стартовый поворот ракеты от ГД-двигателей
    if d["if_povorot_start"] == 1:
        teta = reteta(
            dbell["teta"],
            dbell["x"],
            dbell["y"],
            xc,
            yc,
            d["n_ya"],
            dbell["v"],
            vc,
            tetac,
            direction_law,
            direction_law_preteta,
        )
        # print("TETA = ", teta)
        dbell["teta"] = teta
    # Стартовый участок
    m_0fuel = d["m_0fuel"]
    while m_0fuel > 0:
        t += dt

        xc += vc * cos(tetac)  # Движение цели
        yc += vc * sin(tetac)

        m_0fuel -= d["G_10"] * dt
        dbell["m"] -= d["G_10"] * dt
        L = L_to_point(dbell["x"], dbell["y"], xc, yc)
        if L < d["epsilon"]:
            answer = inf_answer("start")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, True, lcx, lcy)
            return dreturn
        # if(dbell['x'] > xc and dbell['y'] > yc):
        # 	answer = inf_answer("missing")
        # 	dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
        # 	return(dreturn)
        system_equations(dbell)
        if dbell["v"] > d["V_manevr"] and d["flag_startmanevr"] != 0:
            dbell["teta"] = reteta(
                dbell["teta"],
                dbell["x"],
                dbell["y"],
                xc,
                yc,
                d["n_ya"],
                dbell["v"],
                vc,
                tetac,
                direction_law,
                direction_law_preteta,
            )
        if dbell["y"] >= altmax:
            answer = inf_answer("atmosphere")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
            return dreturn
        elif dbell["y"] < 0:
            # print('y = ', dbell['y'])
            # print(dbell)
            print("y = 0 ? Почему???")
            answer = inf_answer("")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, True, lcx, lcy)
            return dreturn
        else:
            rho = atm.f_rho_dra(dbell["y"], dra)
            dbell["rho"] = rho
        lcx.append(xc)
        lcy.append(yc)
        lrx.append(dbell["x"])
        lry.append(dbell["y"])
        lt.append(t)
        lrv.append(dbell["v"])
        lrm.append(dbell["m"])
    # Отстрел стартовой ступени.
    m_sbros = d["m_0"] - d["m_0fuel"]
    if d["if_sbros_march"] == 1:
        t += dt
        dbell["m"] -= m_sbros
        lrm.append(dbell["m"])
        lt.append(t)
        lrx.append(dbell["x"])
        lry.append(dbell["y"])
        lrv.append(dbell["v"])
        lrm.append(dbell["m"])
        lcx.append(xc)
        lcy.append(yc)
    if dbell["v"] / 360 < d["M_start_end"]:
        answer = inf_answer("M<V")
        dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
        return dreturn
    dbell["p"] = d["P_11"]
    # print(dbell)
    print("t = ", t)
    # a = input()
    # Маршевый
    m_1fuel = d["m_1fuel"]
    while m_1fuel > 0:
        t += dt
        xc += vc * cos(tetac)
        yc += vc * sin(tetac)

        m_1fuel -= d["G_11"] * dt
        dbell["m"] -= d["G_11"] * dt
        L = L_to_point(dbell["x"], dbell["y"], xc, yc)
        if L < d["epsilon"]:
            answer = inf_answer("march")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, True, lcx, lcy)
            return dreturn
        # if(dbell['x'] > xc and dbell['y'] > yc):
        # 	answer = inf_answer("missing")
        # 	dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
        # 	return(dreturn)
        system_equations(dbell)
        if dbell["v"] > d["V_manevr"] and d["flag_marchmanevr"] != 0:
            dbell["teta"] = reteta(
                dbell["teta"],
                dbell["x"],
                dbell["y"],
                xc,
                yc,
                d["n_ya"],
                dbell["v"],
                vc,
                tetac,
                direction_law,
                direction_law_preteta,
            )
        if dbell["y"] >= altmax or dbell["y"] < 0:
            answer = inf_answer("atmosphere")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
            return dreturn
        else:
            rho = atm.f_rho_dra(dbell["y"], dra)
            dbell["rho"] = rho
        lcx.append(xc)
        lcy.append(yc)
        lrx.append(dbell["x"])
        lry.append(dbell["y"])
        lt.append(t)
        lrv.append(dbell["v"])
        lrm.append(dbell["m"])
    print("t = ", t)
    # Пассивный
    dbell["p"] = 0
    # mlimit = d["m_1"] - d["m_1fuel"]
    while dbell["v"] / 360 > d["M_passive_end"]:
        t += dt
        xc += vc * cos(tetac)
        yc += vc * sin(tetac)

        L = L_to_point(dbell["x"], dbell["y"], xc, yc)
        if L < d["epsilon"]:
            answer = inf_answer("fatigue")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, True, lcx, lcy)
            return dreturn
        # if(dbell['x'] > xc and dbell['y'] > yc):
        # 	answer = inf_answer("missing")
        # 	dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
        # 	return(dreturn)
        system_equations(dbell)
        if dbell["v"] > d["V_manevr"] and d["flag_passivemanevr"] != 0:
            dbell["teta"] = reteta(
                dbell["teta"],
                dbell["x"],
                dbell["y"],
                xc,
                yc,
                d["n_ya"],
                dbell["v"],
                vc,
                tetac,
                direction_law,
                direction_law_preteta,
            )
        if dbell["y"] >= altmax or dbell["y"] < 0:
            answer = inf_answer("atmosphere")
            dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
            return dreturn
        else:
            rho = atm.f_rho_dra(dbell["y"], dra)
            dbell["rho"] = rho
        lcx.append(xc)
        lcy.append(yc)
        lrx.append(dbell["x"])
        lry.append(dbell["y"])
        lt.append(t)
        lrv.append(dbell["v"])
        lrm.append(dbell["m"])
    print("t = ", t)
    answer = inf_answer("fall")
    dreturn = inf_dreturn(lrx, lry, lt, lrv, lrm, answer, False, lcx, lcy)
    return dreturn
