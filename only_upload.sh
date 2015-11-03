#!/bin/bash
log=/home/pi/test/build.log
date=$(date +%F_%H:%M)
work_dir=/home/pi/test
default=/home/pi/test/default
cd /home/pi/test/
. /home/pi/.bashrc

/usr/bin/avrdude -D -q -V -p atmega2560 -C /etc/avrdude.conf -c stk500v2 -b 115200 -P /dev/ttyUSB0  -U flash:w:$work_dir/build-cli/test.hex:i