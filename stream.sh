#!/bin/bash

#rmmod v4l2loopback
insmod ./v4l2loopback.ko devices=2 video_nr=2 exclusive_caps=1

FILE=/dev/video0

if test -f "$FILE"; then
	echo "video4 has existed"
else
        mv /dev/video0 /dev/video4
	echo "video4 has been generated"
fi

ffmpeg -f video4linux2 -s 320x240 -i /dev/video4 -codec copy -f v4l2 /dev/video2  -codec copy -f v4l2 /dev/video3 >/dev/null 2>&1&

exit 0


