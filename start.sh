#!/bin/bash
cd /home/pi/test/
#python /home/pi/test/app.py
#su pi -c 'bash /home/pi/test/run-redis.sh' &
/home/pi/test/run-redis.sh &
celery worker -A app.celery &
python /home/pi/test/app.py &
#su pi -c 'python /home/pi/test/app.py' &
#su pi -c 'celery worker -A app.celery' &
#sleep 3
#su pi -c 'bash /home/pi/test/build.sh' &
#bash /home/pi/test/stream.sh &
#su pi -c 'bash /home/pi/test/stream.sh' &
/home/pi/test/stream.sh &

exit 0