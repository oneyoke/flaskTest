#!/bin/bash

echo '#include <Arduino.h>' > build-cli/$1.cpp
cat  examples/$2.ino >> build-cli/$1.cpp

/usr/bin/avr-g++ -c -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=100 -I. -I/usr/share/arduino/hardware/arduino/cores/arduino -I/usr/share/arduino/hardware/arduino/variants/mega -I/usr/share/arduino/libraries/LiquidCrystal -I/usr/share/arduino/libraries/DHTlib -I/usr/share/arduino/libraries/Servo -I/usr/share/arduino/libraries/LoLShield -I/home/pi/test/libraries/LiquidCrystal -I/home/pi/test/libraries/DHTlib -I/home/pi/test/libraries/Servo -I/home/pi/test/libraries/LoLShield -g -Os -w -Wall -ffunction-sections -fdata-sections -fno-exceptions build-cli/$1.cpp -o build-cli/$1.o

/usr/bin/avr-gcc -mmcu=atmega2560 -Wl,--gc-sections -Os -o build-cli/$1.elf build-cli/$1.o build-cli/libcore.a  -lc -lm

/usr/bin/avr-objcopy -O ihex -R .eeprom build-cli/$1.elf build-cli/$1.hex