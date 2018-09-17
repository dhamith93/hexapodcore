#!/bin/bash
 
if pgrep mjpg_streamer > /dev/null
then
    echo "mjpg_streamer already running"
else
    cd ~/git/mjpg-streamer/mjpg-streamer-experimental
    ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 640 -y 480 -fps 24 -ex auto -vs -hf" > /dev/null 2>&1&
    echo "mjpg_streamer started"
fi
