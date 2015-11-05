#!/bin/bash
cd /home/pi/test/
log=/home/pi/test/build.log
date=$(date +%F_%H:%M)

echo "$date start build"
cp userino/$1.ino upload.ino
make
#use $@ to print out all arguments at once
#echo $@ ' -> echo $@'
cp build-cli/test.hex userhex/$1.hex
echo "$date build complete"
