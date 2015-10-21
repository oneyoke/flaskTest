#!/bin/bash
cd /home/pi/test/
python /home/pi/test/app.py &
#sleep 3
su pi -c 'bash /home/pi/test/build.sh' &
bash /home/pi/test/stream.sh &
