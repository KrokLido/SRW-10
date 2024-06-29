# Расчёт плоского полёта ракеты.


def dump_tables(d):
    # 1. Расписать файл координат.
    f = open("DUMP_graphic_xy.txt", "w")
    counter = 0

    for elem in d["l_x"]:
        f.write("%s;%s\n" % (elem, d["l_y"][counter]))
        counter += 1
    f.close()

    # 2. Расписать файл масс.
    f = open("DUMP_graphic_m.txt", "w")
    counter = 0
    for elem in d["l_t"]:
        f.write("%s;%s\n" % (elem, d["l_m"][counter]))
        counter += 1
    f.close()

    # 3. Расписать файлы скоростей.
    f = open("DUMP_graphic_vsum.txt", "w")
    counter = 0
    for elem in d["l_V_sum"]:
        f.write("%s;%s\n" % (elem, d["l_t"][counter]))
        counter += 1
    f.close()

    # 4. Расписать файл координат цели.
    f = open("DUMP_graphic_ccxyz.txt", "w")
    counter = 0
    for elem in d["lcx"]:
        f.write("%s;%s\n" % (elem, d["lcy"][counter]))
        counter += 1
    f.close()


def dump_field(dm, name="DUMP_graphic_field_xy.txt"):
    f = open(name, "w")
    for line in dm:
        f.write("%s;%s\n" % (line[0], line[1]))
    f.close()


def support_infrustructure(sbros=False):
    # Подготовка значений.
    dget = {}
    dget = ddata_rocket | ddata_object
    dret = windtower.geometric_calculations(
        dget["m_payload"],
        dget["mu_0"],
        dget["mu_1"],
        dget["yakor_0"],
        dget["yakor_1"],
        dget["I_10"],
        dget["I_11"],
        dget["d"],
        beta=dget["beta"],
    )
    dget = dget | dret
    # print("dget:")
    # for key in dget:
    #    print("\t%s = %s" % (key, dget[key]))
    dget["if_sbros_march"] = dget["flag_sbros_start"]
    if sbros is True:
        dget["if_sbros_march"] = 0
    dget["if_povorot_start"] = dget["flag_startpovorot"]
    dget["dt"] = 0.01
    dget["xc"] = ddata_object["x_0"]
    dget["yc"] = ddata_object["y_0"]
    return dget


def support_infrustructure_for_diff_yakors(yakor_0, yakor_1, sbros=False):
    # Подготовка значений.
    dget = {}
    dget = ddata_rocket | ddata_object
    dget["yakor_0"] = yakor_0
    dget["yakor_1"] = yakor_1
    dret = windtower.geometric_calculations(
        dget["m_payload"],
        dget["mu_0"],
        dget["mu_1"],
        dget["yakor_0"],
        dget["yakor_1"],
        dget["I_10"],
        dget["I_11"],
        dget["d"],
        beta=dget["beta"],
    )
    dget = dget | dret
    # print("dget:")
    # for key in dget:
    #    print("\t%s = %s" % (key, dget[key]))
    dget["if_sbros_march"] = dget["flag_sbros_start"]
    if sbros is True:
        dget["if_sbros_march"] = 0
    dget["if_povorot_start"] = dget["flag_startpovorot"]
    dget["dt"] = 0.01
    dget["xc"] = ddata_object["x_0"]
    dget["yc"] = ddata_object["y_0"]
    return dget


def support_generator(start: float, stop: float, step: float):
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1


if __name__ == "__main__":
    # 1. Составные части.
    print("# 1. Составные части.")
    import windtower  # Содержит в себе функции полёта.
    import libf2  # Содержит в себе функции работы с файлами.

    # import 3d_main_h	# Содержит в себе функции подработки данных, чтобы удобно передать в целевую функцию.
    from sys import argv  # Нужно для получения данных при запуске.

    # 2. Получить данные argv.
    print("# 2. Распаковка данных argv.")
    script, first, second, third = (
        argv  # Нас интересует раздел <first>. Через него будет передаваться флаг на исполнение программы.
    )
    # Через раздел <second> будет изыматься флаг выбора функции решения.

    # 3. Загрузка config.
    print("# 3. Загрузка config.")
    dcfg = libf2.D_FROM_FILE("config")

    # 4. Загрузка данных.
    print("# 4. Загрузка данных.")
    ddata_rocket = libf2.D_FROM_FILE_FLOAT(dcfg["filename_rocket_input"])
    ddata_object = libf2.D_FROM_FILE_FLOAT(dcfg["filename_object_input"])

    # 5. Подготовка значений и запуск программы.
    print("# 5. Подготовка значений и запуск программы.")
    if first == "to_point":
        dget = support_infrustructure()
        print("# ПУСК")
        # ПУСК.
        dfrom = windtower.main_system(dget)

        # Анализ решения.
        print("# Анализ решения.")
        print(dfrom["answer"])
        print("x_r = %s,\ty_r = %s" % (dfrom["l_x"][-1], dfrom["l_y"][-1]))
        print("x_c = %s,\ty_c = %s" % (dfrom["lcx"][-1], dfrom["lcy"][-1]))

        # Сброс данных в файл.
        dump_tables(dfrom)

    elif first == "fields":
        # Подготовка значений.
        dget = support_infrustructure()
        print("# ПУСК")

        # Массив найденных точек.
        array_ans = []
        # Создание полей.
        limx = dget["field_limx"]
        limy = dget["field_limy"]
        counter = 0
        iter_x = -limx
        while iter_x <= limx:
            dget["xc"] = iter_x
            iter_y = 100
            while iter_y <= limy:
                counter += 1
                dget["yc"] = iter_y
                print("# ПУСК по цели: xc = %s\tyc = %s" % (iter_x, iter_y))
                dfrom = windtower.main_system(dget)
                print("dfrom['flag'] == ", dfrom["flag"])
                print("dfrom['answer'] == ", dfrom["answer"])
                if dfrom["flag"]:  # Если вдруг решение прошло, то его следует сохранить.
                    print(dfrom["answer"])
                    l_ans = {}
                    l_ans["field_direct"] = counter
                    l_ans["flag"] = dfrom["flag"]
                    l_ans["iter_x"] = iter_x
                    l_ans["iter_y"] = iter_y
                    array_ans.append(l_ans)
                    # Генерация файла с сохранённым решением.
                    # fname = "field_direct_" + str(counter)
                    # f = open(fname, 'w')
                    # substring = 'flag:\t' + str(dfrom['flag']) + '\n'
                    # f.write(substring)
                    # substring = 'iter_x:\t' + str(iter_x) + '\n'
                    # f.write(substring)
                    # substring = 'iter_y:\t' + str(iter_y) + '\n'
                    # f.write(substring)
                    # substring = 'iter_z:\t' + str(iter_z) + '\n'
                    # f.write(substring)
                    # f.close()
                iter_y += 1000
            iter_x += 1000
        # Сохранение результатов в файл.
        f = open("field_direct", "w")
        for elem in array_ans:
            # Нужно записать каждый элемент.
            substring = "=" * 10 + "\n"
            f.write(substring)
            substring = "flag:\t" + str(elem["flag"]) + "\n"
            f.write(substring)
            substring = "iter_x:\t" + str(elem["iter_x"]) + "\n"
            f.write(substring)
            substring = "iter_y:\t" + str(elem["iter_y"]) + "\n"
            f.write(substring)
        f.close()
        # Оформление данных для построени графиков
        ret = []
        for elem in array_ans:
            if elem["flag"] != True:
                continue
            bufer = []
            bufer.append(elem["iter_x"])
            bufer.append(elem["iter_y"])
            ret.append(bufer)
        dump_field(ret)
    elif first == "fields_interceptor":
        # Заглушка для вызова программы на построение поля пуска-поражения цели с заданной скоростью и направлением движения.
        dget = support_infrustructure()
        limx = dget["field_limx"]
        limy = dget["field_limy"]
        genxc = support_generator(-limx, limx, 1000)
        axc = []
        genyc = support_generator(100, limy, 1000)
        ayc = []
        for i in genxc:
            axc.append(i)
        for i in genyc:
            ayc.append(i)
        gen1 = support_generator(100, 2500, 500)
        for vci in gen1:
            array_ans = []
            for xci in axc:
                dget["xc"] = xci
                for yci in ayc:
                    dget["yc"] = yci
                    print(
                        "# ПУСК по цели: vci = %s,\txc = %s,\tyc = %s" % (vci, xci, yci)
                    )
                    dfrom = windtower.main_system(dget)
                    print("dfrom['flag'] == ", dfrom["flag"])
                    print("dfrom['answer'] == ", dfrom["answer"])
                    if dfrom[
                        "flag"
                    ]:  # Если вдруг решение прошло, то его следует сохранить.
                        print(dfrom["answer"])
                        l_ans = {}
                        l_ans["flag"] = dfrom["flag"]
                        l_ans["iter_x"] = xci
                        l_ans["iter_y"] = yci
                        array_ans.append(l_ans)
            # Оформление данных для построения графиков
            name = "RESULT_field_vci_" + str(vci) + ".txt"
            ret = []
            for elem in array_ans:
                if elem["flag"] != True:
                    continue
                bufer = []
                bufer.append(elem["iter_x"])
                bufer.append(elem["iter_y"])
                ret.append(bufer)
            dump_field(ret, name)
    elif first == "character":
        # Заглушка для нахождения характеристик ракеты по заданным дальностям полёта с нахождением таблиц данных для обстрела всех возможных скоростей целей.
        # print("# ПУСК")
        ddata_object["vc"] = 0
        # 1. Нужно итеративно менять mu_0, mu_1, при заданных yakor_0, yakor_1, чтобы подобрать требуемую массу топлива.
        best = {}
        best["m_sum"] = None
        best["mu_0"] = None
        best["mu_1"] = None
        # Генерация значений
        gen1 = support_generator(0.1, 0.6, 0.005)
        gen2 = support_generator(0.1, 0.5, 0.005)
        arimu0 = []
        arimu1 = []
        for i in gen1:
            arimu0.append(i)
        for i in gen2:
            arimu1.append(i)
        for imu0 in arimu0:
            ddata_rocket["mu_0"] = imu0
            for imu1 in arimu1:
                print("imu0 = %s, imu1 = %s" % (imu0, imu1))
                ddata_rocket["mu_1"] = imu1
                if second == "without":
                    dget = support_infrustructure(sbros=False)
                else:
                    dget = support_infrustructure()
                dfrom = windtower.main_system(dget)
                if dfrom["flag"]:
                    print(dfrom["answer"])
                    if best["m_sum"] is None:
                        best["m_sum"] = dget["m_sum"]
                        best["mu_0"] = imu0
                        best["mu_1"] = imu1
                    elif best["m_sum"] > dget["m_sum"]:
                        best["m_sum"] = dget["m_sum"]
                        best["mu_0"] = imu0
                        best["mu_1"] = imu1
        f = open("RESULT_character.txt", "w")
        substring = "m:\t" + str(best["m_sum"]) + "\n"
        print(substring)
        f.write(substring)
        substring = "mu_0:\t" + str(best["mu_0"]) + "\n"
        print(substring)
        f.write(substring)
        substring = "mu_1:\t" + str(best["mu_1"]) + "\n"
        print(substring)
        f.write(substring)
        f.close()

        ddata_rocket["mu_0"] = best["mu_0"]
        ddata_rocket["mu_1"] = best["mu_1"]
        dget = support_infrustructure()
        get = windtower.main_system(dget)
        dump_tables(get)
    elif first == "two_point":
        preteta = float(second)
        dget = support_infrustructure()
        dget["direction_law"] = "2_point_preteta"
        dget["direction_law_preteta"] = preteta
        print("# ПУСК")
        # ПУСК.
        dfrom = windtower.main_system(dget)

        # Анализ решения.
        print("# Анализ решения.")
        print(dfrom["answer"])
        print("x_r = %s,\ty_r = %s" % (dfrom["l_x"][-1], dfrom["l_y"][-1]))
        print("x_c = %s,\ty_c = %s" % (dfrom["lcx"][-1], dfrom["lcy"][-1]))

        # Сброс данных в файл.
        dump_tables(dfrom)
    elif first == "two_point_field":
        # Подготовка значений.
        dget = support_infrustructure()
        # print("# ПУСК")
        preteta = float(second)
        dget["direction_law"] = "2_point_preteta"
        dget["direction_law_preteta"] = preteta
        # Массив найденных точек.
        array_ans = []
        # Создание полей.
        limx = dget["field_limx"]
        limy = dget["field_limy"]
        counter = 0
        iter_x = -limx
        while iter_x <= limx:
            dget["xc"] = iter_x
            iter_y = 100
            while iter_y <= limy:
                counter += 1
                dget["yc"] = iter_y
                # print("# ПУСК по цели: xc = %s\tyc = %s" % (iter_x, iter_y))
                dfrom = windtower.main_system(dget)
                # print("dfrom['flag'] == ", dfrom["flag"])
                # print("dfrom['answer'] == ", dfrom["answer"])
                if dfrom["flag"]:  # Если вдруг решение прошло, то его следует сохранить.
                    # print(dfrom["answer"])
                    l_ans = {}
                    l_ans["field_direct"] = counter
                    l_ans["flag"] = dfrom["flag"]
                    l_ans["iter_x"] = iter_x
                    l_ans["iter_y"] = iter_y
                    array_ans.append(l_ans)
                    # Генерация файла с сохранённым решением.
                    # fname = "field_direct_" + str(counter)
                    # f = open(fname, 'w')
                    # substring = 'flag:\t' + str(dfrom['flag']) + '\n'
                    # f.write(substring)
                    # substring = 'iter_x:\t' + str(iter_x) + '\n'
                    # f.write(substring)
                    # substring = 'iter_y:\t' + str(iter_y) + '\n'
                    # f.write(substring)
                    # substring = 'iter_z:\t' + str(iter_z) + '\n'
                    # f.write(substring)
                    # f.close()
                iter_y += 1000
            iter_x += 1000
        # Сохранение результатов в файл.
        f = open("field_direct", "w")
        for elem in array_ans:
            # Нужно записать каждый элемент.
            substring = "=" * 10 + "\n"
            f.write(substring)
            substring = "flag:\t" + str(elem["flag"]) + "\n"
            f.write(substring)
            substring = "iter_x:\t" + str(elem["iter_x"]) + "\n"
            f.write(substring)
            substring = "iter_y:\t" + str(elem["iter_y"]) + "\n"
            f.write(substring)
        f.close()
        # Оформление данных для построени графиков
        ret = []
        for elem in array_ans:
            if elem["flag"] != True:
                continue
            bufer = []
            bufer.append(elem["iter_x"])
            bufer.append(elem["iter_y"])
            ret.append(bufer)
        dump_field(ret)
    elif first == "parallel":
        if second == "without":
            dget = support_infrustructure(sbros=False)
        else:
            dget = support_infrustructure()
        dget["direction_law"] = "parallel"
        dget["direction_law_preteta"] = 0
        print("# ПУСК")
        # ПУСК.
        dfrom = windtower.main_system(dget)

        # Анализ решения.
        print("# Анализ решения.")
        print(dfrom["answer"])
        print("x_r = %s,\ty_r = %s" % (dfrom["l_x"][-1], dfrom["l_y"][-1]))
        print("x_c = %s,\ty_c = %s" % (dfrom["lcx"][-1], dfrom["lcy"][-1]))

        # Сброс данных в файл.
        dump_tables(dfrom)
    elif first == "parallel_field":
        # Подготовка значений.
        dget = support_infrustructure()
        # print("# ПУСК")
        dget["direction_law"] = "parallel"
        dget["direction_law_preteta"] = 0
        # Массив найденных точек.
        array_ans = []
        # Создание полей.
        limx = dget["field_limx"]
        limy = dget["field_limy"]
        counter = 0
        iter_x = -limx
        while iter_x <= limx:
            dget["xc"] = iter_x
            iter_y = 100
            while iter_y <= limy:
                counter += 1
                dget["yc"] = iter_y
                # print("# ПУСК по цели: xc = %s\tyc = %s" % (iter_x, iter_y))
                dfrom = windtower.main_system(dget)
                # print("dfrom['flag'] == ", dfrom["flag"])
                # print("dfrom['answer'] == ", dfrom["answer"])
                if dfrom["flag"]:  # Если вдруг решение прошло, то его следует сохранить.
                    # print(dfrom["answer"])
                    l_ans = {}
                    l_ans["field_direct"] = counter
                    l_ans["flag"] = dfrom["flag"]
                    l_ans["iter_x"] = iter_x
                    l_ans["iter_y"] = iter_y
                    array_ans.append(l_ans)
                    # Генерация файла с сохранённым решением.
                    # fname = "field_direct_" + str(counter)
                    # f = open(fname, 'w')
                    # substring = 'flag:\t' + str(dfrom['flag']) + '\n'
                    # f.write(substring)
                    # substring = 'iter_x:\t' + str(iter_x) + '\n'
                    # f.write(substring)
                    # substring = 'iter_y:\t' + str(iter_y) + '\n'
                    # f.write(substring)
                    # substring = 'iter_z:\t' + str(iter_z) + '\n'
                    # f.write(substring)
                    # f.close()
                iter_y += 1000
            iter_x += 1000
        # Сохранение результатов в файл.
        f = open("field_direct", "w")
        for elem in array_ans:
            # Нужно записать каждый элемент.
            substring = "=" * 10 + "\n"
            f.write(substring)
            substring = "flag:\t" + str(elem["flag"]) + "\n"
            f.write(substring)
            substring = "iter_x:\t" + str(elem["iter_x"]) + "\n"
            f.write(substring)
            substring = "iter_y:\t" + str(elem["iter_y"]) + "\n"
            f.write(substring)
        f.close()
        # Оформление данных для построени графиков
        ret = []
        for elem in array_ans:
            if elem["flag"] != True:
                continue
            bufer = []
            bufer.append(elem["iter_x"])
            bufer.append(elem["iter_y"])
            ret.append(bufer)
        dump_field(ret)
    elif first == "parallel_field_different":
        # Подготовка значений.
        if third == "without":
            dget = support_infrustructure(sbros=True)
        else:
            dget = support_infrustructure()
        # Подмена полученной скорости
        dget["vc"] = float(second)
        # print("# ПУСК")
        dget["direction_law"] = "parallel"
        dget["direction_law_preteta"] = 0
        # Массив найденных точек.
        array_ans = []
        # Создание полей.
        limx = dget["field_limx"]
        limy = dget["field_limy"]
        counter = 0
        iter_x = -limx
        while iter_x <= limx:
            dget["xc"] = iter_x
            iter_y = 100
            while iter_y <= limy:
                counter += 1
                dget["yc"] = iter_y
                # print("# ПУСК по цели: xc = %s\tyc = %s" % (iter_x, iter_y))
                dfrom = windtower.main_system(dget)
                # print("dfrom['flag'] == ", dfrom["flag"])
                # print("dfrom['answer'] == ", dfrom["answer"])
                if dfrom["flag"]:  # Если вдруг решение прошло, то его следует сохранить.
                    # print(dfrom["answer"])
                    l_ans = {}
                    l_ans["field_direct"] = counter
                    l_ans["flag"] = dfrom["flag"]
                    l_ans["iter_x"] = iter_x
                    l_ans["iter_y"] = iter_y
                    array_ans.append(l_ans)
                    # Генерация файла с сохранённым решением.
                    # fname = "field_direct_" + str(counter)
                    # f = open(fname, 'w')
                    # substring = 'flag:\t' + str(dfrom['flag']) + '\n'
                    # f.write(substring)
                    # substring = 'iter_x:\t' + str(iter_x) + '\n'
                    # f.write(substring)
                    # substring = 'iter_y:\t' + str(iter_y) + '\n'
                    # f.write(substring)
                    # substring = 'iter_z:\t' + str(iter_z) + '\n'
                    # f.write(substring)
                    # f.close()
                iter_y += 1000
            iter_x += 1000
        # Сохранение результатов в файл.
        f = open("field_direct", "w")
        for elem in array_ans:
            # Нужно записать каждый элемент.
            substring = "=" * 10 + "\n"
            f.write(substring)
            substring = "flag:\t" + str(elem["flag"]) + "\n"
            f.write(substring)
            substring = "iter_x:\t" + str(elem["iter_x"]) + "\n"
            f.write(substring)
            substring = "iter_y:\t" + str(elem["iter_y"]) + "\n"
            f.write(substring)
        f.close()
        # Оформление данных для построени графиков
        ret = []
        for elem in array_ans:
            if elem["flag"] != True:
                continue
            bufer = []
            bufer.append(elem["iter_x"])
            bufer.append(elem["iter_y"])
            ret.append(bufer)
        dump_field(ret)

    elif first == "srw1_character":
        # Заглушка для нахождения характеристик ракеты по заданным дальностям полёта с нахождением таблиц данных для обстрела всех возможных скоростей целей по заданным тяговооружённостям.
        # На позициях <second> и <third> прилетает тяговооружённость стартового и маршевого режима (или ступеней) соответственно.
        # Нужно обработать значения тяговооружённостей, чтобы нормально вытаскивать значения.
        second = second.replace(",", ".")
        third = third.replace(",", ".")
        ddata_object["vc"] = 0
        # 1. Нужно итеративно менять mu_0, mu_1, при заданных yakor_0, yakor_1, чтобы подобрать требуемую массу топлива.
        best = {}
        best["m_sum"] = None
        best["mu_0"] = None
        best["mu_1"] = None
        # Генерация значений
        gen1 = support_generator(0.1, 0.6, 0.005)
        gen2 = support_generator(0.1, 0.5, 0.005)
        arimu0 = []
        arimu1 = []
        for i in gen1:
            arimu0.append(i)
        for i in gen2:
            arimu1.append(i)
        for imu0 in arimu0:
            ddata_rocket["mu_0"] = imu0
            for imu1 in arimu1:
                # print("imu0 = %s, imu1 = %s" % (imu0, imu1))
                ddata_rocket["mu_1"] = imu1
                dget = support_infrustructure_for_diff_yakors(float(second), float(third))
                dfrom = windtower.main_system(dget)
                if dfrom["flag"]:
                    # print(dfrom["answer"])
                    if best["m_sum"] is None:
                        best["m_sum"] = dget["m_sum"]
                        best["mu_0"] = imu0
                        best["mu_1"] = imu1
                    elif best["m_sum"] > dget["m_sum"]:
                        best["m_sum"] = dget["m_sum"]
                        best["mu_0"] = imu0
                        best["mu_1"] = imu1
        f = open("RESULT_character.txt", "w")
        substring = "m:\t" + str(best["m_sum"]) + "\n"
        # print(substring)
        f.write(substring)
        substring = "mu_0:\t" + str(best["mu_0"]) + "\n"
        # print(substring)
        f.write(substring)
        substring = "mu_1:\t" + str(best["mu_1"]) + "\n"
        # print(substring)
        f.write(substring)
        f.close()

        ddata_rocket["mu_0"] = best["mu_0"]
        ddata_rocket["mu_1"] = best["mu_1"]
        dget = support_infrustructure()
        get = windtower.main_system(dget)
        dump_tables(get)
