#!/bin/bash


W1DIR="/sys/bus/w1/devices"
date=$(date)
work_dir="/home/pi/test"
flag=0
if (( $(cat /sys/class/gpio/gpio23/value) > 0 ))
then
	critical=35
else
	critical=43
fi


# Exit if 1-wire directory does not exist
if [ ! -d $W1DIR ]
then
	flag=$flag+1
	echo "Can't find 1-wire device directory">>$work_dir/therm.log
else


# Get a list of all devices
DEVICES=$(ls $W1DIR)
if (( $DEVICES < 2 )) 
then
	flag=$flag+1
fi

# Loop through all devices
for DEVICE in $DEVICES
do
	# Ignore the bus master device
	if [ $DEVICE != "w1_bus_master1" ]
	then
		# Get an answer from this device
		ANSWER=$(cat $W1DIR/$DEVICE/w1_slave)

		# See if device really answered
		# When a previously existing device is removed it will	
		# read 00 00 00 00 00 00 00 00 00, which results in a
		# valid CRC. That's why we need this extra test.
		echo -e "$ANSWER" | grep -q "00 00 00 00 00 00 00 00 00"

		if [ $? -ne 0 ]
		then
			# The temperature is only valid if the CRC matches
			echo -e "$ANSWER" | grep -q "YES"
			if [ $? -eq 0 ]
			then
				# Isolate the temprature from the second line
				TEMPERATURE=$(echo -e "$ANSWER" | grep "t=" | cut -f 2 -d "=")
				# Isolate integer and fraction parts so we know where
				# the decimal point should go
				INTEGER=${TEMPERATURE:0:(-3)}
				FRACTION=${TEMPERATURE:(-3)}

				# Restore the leading 0 for positive and negative numbers
				if [ -z $INTEGER ]
				then
					INTEGER="0"
				fi
				if [ "$INTEGER" == "-" ]
				then
					INTEGER="-0"
				fi
				date=$(date)
				# Write result of this sensor
#				echo "$date $DEVICE=$INTEGER.$FRACTION">>$work_dir/therm.log
				if (($INTEGER>$critical))
				then 
					flag=$falg+1
					echo "$date $DEVICE=$INTEGER.$FRACTION">>$work_dir/therm.log
				fi
			else
				# A CRC was found, show error message instead
				echo "$DEVICE=CRC error">>$work_dir/therm.log
				flag=$flag+1
			fi
		fi
	fi
done
fi

if (( flag>0 ))
then
	echo "power off">>$work_dir/therm.log
        $work_dir/gpio.sh 23 1
        $work_dir/gpio.sh 18 1

else
        echo "power on">>$work_dir/therm.log
        $work_dir/gpio.sh 23 0
        $work_dir/gpio.sh 18 0
fi
