#!/bin/bash
# set below your Raspberry PI IP address
myip="109.123.177.216"
port="5001"


#gst-launch -v v4l2src ! 'video/x-raw-yuv,width=640,height=480',framerate=30/1 ! ffmpegcolorspace ! x264enc ! rtph264pay ! udpsink host=$myip port=$port 

#mjpeg ok
gst-launch -v v4l2src ! "image/jpeg,width=1280,height=720,framerate=15/1" ! multipartmux ! tcpserversink host=$myip port=$port sync=false


#h264
#gst-launch -v v4l2src ! 'video/x-raw-yuv,width=640,height=480' !  x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink  host=$myip port=$port

# gst-launch v4l2src ! "video/x-raw-yuv,width=1280,height=720" ! ffmpegcolorspace ! ffenc_h263 ! video/x-h263 ! rtph263ppay pt=96 ! udpsink host=$myip port=$port sync=false 
