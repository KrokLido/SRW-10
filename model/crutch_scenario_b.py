# Осуществляет генерацию разных файлов данных для ракеты.


def support_generator(start: float, stop: float, step: float):
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1


if __name__ == "__main__":
    from sys import argv

    script, first = argv
    import libf2

    data_rocket = libf2.D_FROM_FILE_FLOAT(str(first))  # Загрузили данные.
    gen1 = support_generator(2, 20, 0.5)
    gen2 = support_generator(1, 20, 0.5)
    agyakor0 = []
    agyakor1 = []
    for i in gen1:
        agyakor0.append(i)
    for i in gen2:
        agyakor1.append(i)
    counter = 0
    for yi0 in agyakor0:
        for yi1 in agyakor1:
            counter += 1
            data_rocket["yakor_0"] = yi0
            data_rocket["yakor_1"] = yi1
            fname = "config_rocket_remake_" + str(counter)
            libf2.D_IN_FILE_FLOAT(fname, data_rocket)
