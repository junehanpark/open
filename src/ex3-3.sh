#!/bin/sh

weight=$1
height=$2

height_square=$(($height * $height))
bmi=$(($weight * 100000 / $height_square))

if [ $bmi -le 185 ]; then
	echo "low wheight"
elif [ $bmi -lt 230 ]; then
	echo "normal wheight"
else 
	echo "over wheight"
fi

exit 0
