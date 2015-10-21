#!/bin/bash

gpio=$1
value=$2

#if ((1))
if ((!$(ls -1 /sys/class/gpio/ | grep gpio$gpio | wc -l)))
   then echo $gpio | sudo tee /sys/class/gpio/export
fi

if (( !$(cat "/sys/class/gpio/gpio$gpio/direction" | grep out | wc -l) ))
then 
	echo out | sudo tee  /sys/class/gpio/gpio$gpio/direction
fi
echo  $value | sudo tee /sys/class/gpio/gpio$gpio/value
