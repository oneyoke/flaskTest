#!/bin/bash
log=/home/pi/test/build.log
date=$(date +%F_%H:%M)
work_dir=/home/pi/test
default=/home/pi/test/default
cd /home/pi/test/
. /home/pi/.bashrc
#PATH=$work_dir
while :
do
#sleep 5
#./gpio.sh 17 1
#if (( $(ls | grep upload1.ino | wc -l)>0 ))
#then 
#if (( $(ps aux | grep build.sh | wc -l) < 4 ))
#then
	inotifywait $work_dir/upload.ino
	$work_dir/therm.sh
	$work_dir/gpio.sh 17 1
	echo "$date start build" > $log
	make >> $log
	echo "$date build complete" >> $log
	sleep 2
#	make upload >> $log
        while (( $( /usr/bin/avrdude -D -q -V -p atmega2560 -C /etc/avrdude.conf -c stk500v2 -b 115200 -P /dev/ttyUSB0  -U flash:w:$work_dir/build-cli/test.hex:i 2>&1 > /dev/null | grep error | wc -l) > 0 ))
	do
	sleep 3
	n=$n+1
	done

#	/usr/bin/avrdude -F -q -V -D -p atmega328p -C /etc/avrdude.conf -c arduino -b 115200 -P /dev/ttyACM0 -U flash:w:/home/pi/test/build-cli/test.hex:i >> $log
	cp -f "$work_dir/upload.ino" "$work_dir/old/$date.ino" >> $log
	cp -f "$default/default.ino" "$work_dir/upload.ino" >> $log
        $work_dir/gpio.sh 17 0
	sleep 30
	echo "$date default program upload"
        $work_dir/gpio.sh 17 1
	cp $default/test.hex "$work_dir/build-cli/test.hex" >> $log
        while (( $( /usr/bin/avrdude -D -q -V -p atmega2560 -C /etc/avrdude.conf -c stk500v2 -b 115200 -P /dev/ttyUSB0  -U flash:w:$work_dir/build-cli/test.hex:i 2>&1 > /dev/null | grep error | wc -l) > 0 ))
	do
	sleep 3
	n=$n+1
	done

# 	/usr/bin/avrdude -F -q -V -D -p atmega328p -C /etc/avrdude.conf -c arduino -b 115200 -P /dev/ttyACM0 -U flash:w:/home/pi/test/build-cli/test.hex:i >> $log	
#	make upload >> $log
#	$work_dir/gpio.sh 17 0
#fi
#./gpio.sh 17 0

done
