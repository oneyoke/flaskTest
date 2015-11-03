#!/bin/bash
cd /home/pi/test/
log=/home/pi/test/build.log
date=$(date +%F_%H:%M)

echo "$date start build"
make
echo "$date build complete"
