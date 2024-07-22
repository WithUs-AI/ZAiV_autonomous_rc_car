#!/bin/bash

sudo modprobe hailo_pci
export DISPLAY=:0
export LIBCAMERA_RPI_TUNING_FILE=/home/pi/Work/rc/imx219_175/imx219_160_v2.json

echo  "1. mp4   2. cam"

echo -n "set mod: "
read mod

# 입력값이 비어있는지 확인
if [ -z "$mod" ]; then
  echo "Error: No name provided"
  exit 1
fi

# 공백이 있는 경우를 처리
mod="${mod// /_}"



if [ "$mod" == "mp4" ] || [ "$mod" == "video" ]; then
    PIPELINE="gst-launch-1.0 -v filesrc location=/home/pi/Work/rc/imx219_175/video/test2-converted.mp4 name=src_0 ! qtdemux ! h264parse ! avdec_h264 max_threads=2 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoscale n-threads=2 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailonet hef-path=/home/pi/Work/rc/imx219_175/config/rc_hose_300.hef batch-size=1 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailofilter function-name=yolov5 config-path=/home/pi/Work/rc/imx219_175/config/yolov5_rc_hose.json so-path=/home/pi/Work/rc/imx219_175/config/libyolo_post.so qos=false ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailooverlay ! hailoexportzmq ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 ! fpsdisplaysink video-sink=ximagesink name=hailo_display sync=false text-overlay=true"
else
    PIPELINE="gst-launch-1.0 -v libcamerasrc camera-name=\"/base/soc/i2c0mux/i2c@1/imx219@10\" ! video/x-raw, width=1600, height=1200, framerate=41/1 ! queue ! videoscale ! video/x-raw, width=640, height=480 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoscale n-threads=2 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailonet hef-path=/home/pi/Work/rc/imx219_175/config/rc_hose_300.hef batch-size=1 ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailofilter function-name=yolov5 config-path=/home/pi/Work/rc/imx219_175/config/yolov5_rc_hose.json so-path=/home/pi/Work/rc/imx219_175/config/libyolo_post.so qos=false ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! hailooverlay ! hailoexportzmq ! queue max-size-buffers=5 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 ! fpsdisplaysink video-sink=ximagesink name=hailo_display sync=false text-overlay=true"
fi

# SIGINT (Ctrl+C)를 대기하고 처리하는 함수
trap "echo Stopping...; kill $PID; exit" SIGINT

# 무한 루프를 사용하여 파이프라인을 반복 실행
while true
do
    $PIPELINE &
    PID=$!
    
    # 파이프라인이 실행되는 동안 대기
    wait $PID
done