#!/bin/bash

function _prestart {
echo "Function _prestart on run..."
rm SRW-1*
}


function black_flake8 {
echo "Function blake_flake8 on run..."
python3.11 -m black *
python3.11 -m flake8 *
}


# Prestart
rm SRW-1*
rm DUMP*
python3.11 -m black *.py
python3.11 -m flake8 *.py


# This is a comment
echo "Shell scrypt run..."
echo "Variants of desicions:"
echo "a = ВЫСТРЕЛ Простая пристрелка(to_point light)"
echo "b = ПОДБОР Вычисление внешнебаллистических характеристик"
echo "c = ПОЛЕ Построение полей по располагаемым характеристикам(fields to_point)"
echo "d = ПОЛЕ Построение полей по быстролетящим(более 100 м/с) целям"
echo "e = ВЫСТРЕЛ Пристрелка по закону наведения по двум точкам с дистанцией упреждения"
echo "f = ПОЛЕ Построение полей по располагаемым характеристикам(fields 2_point_prelength)"
echo 'g = ВЫСТРЕЛ самонаведение по методу параллельного сближения с целью'
echo 'gf = ПОЛЕ параллельное сближение с целью'
echo 'gfd = ПОЛЯ стрельбы по целям со скоростью 100, 600, 1000 м/с.'

read readed1 readed2
echo "readed1 = $readed1"
echo "readed2 = $readed2"

#	READED "A"
if [ $readed1 = "a" ]
then
echo "Readed 'a'..."
python3.11 2d_main.py to_point None

gnuplot graphic_xy.gpi
gnuplot graphic_m.gpi
gnuplot graphic_vsum.gpi

#rm DUMP*
okular SRW-1_Vr_sum.jpg
okular SRW-1_xy.jpg
okular SRW-1_m.jpg

#	READED "B"
elif [ $readed1 = "b" ]
then 
rm DUMP*
python3.11 2d_main.py character None

gnuplot graphic_xy.gpi
gnuplot graphic_m.gpi
gnuplot graphic_vsum.gpi

#rm DUMP*
okular SRW-1_Vr_sum.jpg
okular SRW-1_xy.jpg
okular SRW-1_m.jpg


#	READED "C"
elif [ $readed1 = "c" ]
then
python3.11 2d_main.py fields to_point

gnuplot graphic_fields.gpi
rm DUMP*
okular SRW-1_field_xy.jpg
#okular SRW-1_field.xz.jpg
#okular SRW-1_field.yz.jpg


#	READED "D"
elif [ $readed1 = "d" ]
then
python3.11 2d_main.py fields_interceptor None



#	READED "E"
elif [ $readed1 = 'e' ]
then
python3.11 2d_main.py two_point $readed2

gnuplot graphic_xy.gpi
gnuplot graphic_m.gpi
gnuplot graphic_vsum.gpi

okular SRW-1_Vr_sum.jpg
okular SRW-1_xy.jpg
okular SRW-1_m.jpg



#	READED "F"
elif [ $readed1 = 'f' ]
then
python3.11 2d_main.py two_point_field $readed2

gnuplot graphic_fields.gpi
rm DUMP*
okular SRW-1_field_xy.jpg


# 	READED "G"
elif [ $readed1 = 'g' ]
then
python3.11 2d_main.py parallel None

gnuplot graphic_xy.gpi
gnuplot graphic_m.gpi
gnuplot graphic_vsum.gpi

okular SRW-1_Vr_sum.jpg
okular SRW-1_xy.jpg
okular SRW-1_m.jpg

mkdir scenario_g
mv SRW-1* scenario_g

# 	READED "GF"
elif [ $readed1 = 'gf' ]
then
python3.11 2d_main.py parallel_field None
gnuplot graphic_fields.gpi
rm DUMP*
okular SRW-1_field_xy.jpg

#	READED "GFD"
elif [ $readed1 = 'gfd' ]
then
python3.11 2d_main.py parallel_field_different 1
gnuplot graphic_fields.gpi
rm DUMP*
#okular SRW-1_field_xy.jpg
cp SRW-1_field_xy.jpg SRW-1_field_xy_1.jpg
mkdir scenario_gfd
mv SRW-1_field_xy_1.jpg ./scenario_gfd

python3.11 2d_main.py parallel_field_different 6
gnuplot graphic_fields.gpi
rm DUMP*
cp SRW-1_field_xy.jpg SRW-1_field_xy_6.jpg
mv SRW-1_field_xy_6.jpg ./scenario_gfd


python3.11 2d_main.py parallel_field_different 10
gnuplot graphic_fields.gpi
rm DUMP*
cp SRW-1_field_xy.jpg SRW-1_field_xy_10.jpg
mv SRW-1_field_xy_10.jpg ./scenario_gfd
rm SRW-1_field_xy.jpg

fi

echo "End of shell-code."
