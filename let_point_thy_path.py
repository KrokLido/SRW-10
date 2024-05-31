#
#
#
#
#
# 	ЗДЕСЬ ТОЛЬКО НАВЕДЕНИЕ И БОЛЕЕ НИЧЕГО.
#
#
#
#
#
import math
from trigonometria import cos, sin

# 	=	Объёмный мир	=


# Процедура вычисляет угол линии по двум точкам к горизонту. Для плоской задачи.
# Получает:                                     4 координаты:
#                                                               -       xc              - координата x цели.
#                                                               -       yc              - координата y цели.
#                                                               -       xr              - координата x ракеты.
#                                                               -       yr              - координата y ракеты.
# Делает:                                       Вычисляет угол.
# Возвращает:                           угол.
def water_teta(xc, yc, xr, yr, flag_psi=False):
    y = yc - yr
    x = xc - xr
    if x == 0:
        if y > 0:
            return 90
        elif y < 0:
            return -90
        else:
            return 0
    if y == 0:
        teta = 0
        return 0
    teta = y / x
    if (x > 0) and (y > 0):
        rad = math.atan(teta)
        return math.degrees(rad)
    if (x < 0) and (y > 0):
        rad = math.atan(teta)
        return math.degrees(rad) + 180
    if (x < 0) and (y < 0):
        rad = math.atan(teta)
        if flag_psi == False:
            return math.degrees(rad) - 180
        return math.degrees(rad) - 180
    if (x > 0) and (y < 0):
        rad = math.atan(teta)
        return math.degrees(rad)


if __name__ == "__main__":
    for xci in range(-20000, 20001):
        teta = water_teta(xci, 20000, 0, 0)
        print(
            "xci = %s, yci = %s, xr = %s, yr = %s, teta = %s" % (xci, 20000, 0, 0, teta)
        )
