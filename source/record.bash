#!/bin/bash

export DISPLAY=:0
export LIBCAMERA_RPI_TUNING_FILE=/home/pi/Work/rc/imx219_175/imx219_160_v2.json

# echo "mp4 name: "
# read name
# echo "mp4 name: $name.mp4"

echo -n "mp4 name: "
read name

# 입력값이 비어있는지 확인
if [ -z "$name" ]; then
  echo "Error: No name provided"
  exit 1
fi

# 공백이 있는 경우를 처리
name="${name// /_}"

echo "mp4 name: $name.mp4"



# 파이프라인 정의
#PIPELINE="gst-launch-1.0 libcamerasrc camera-name="/base/soc/i2c0mux/i2c@0/ov5647@36" ! video/x-raw, width=640, height=480, framerate=58/1 ! videoconvert ! queue ! x264enc ! mp4mux fragment-duration=500 ! filesink location=$name.mp4"
#PIPELINE="gst-launch-1.0 libcamerasrc camera-name="/base/soc/i2c0mux/i2c@0/ov5647@36" ! video/x-raw, width=640, height=480, framerate=58/1 ! videoconvert ! queue ! x264enc tune=zerolatency ! mp4mux fragment-duration=100 ! filesink location=$name.mp4"
#PIPELINE="gst-launch-1.0 libcamerasrc camera-name="/base/soc/i2c0mux/i2c\@0/imx219\@10" ! video/x-raw, width=640, height=480, framerate=58/1 ! videoconvert ! queue ! x264enc ! mp4mux fragment-duration=100 ! filesink location=$name.mp4"
PIPELINE="gst-launch-1.0 -v libcamerasrc camera-name="/base/soc/i2c0mux/i2c\@1/imx219\@10" ! video/x-raw, width=1600, height=1200, framerate=40/1 ! videoscale ! video/x-raw, width=640, height=480 ! videoconvert ! queue ! x264enc ! mp4mux fragment-duration=100 ! filesink location=./video/$name.mp4"



# 파이프라인 실행 및 백그라운드에서 실행되는 PID 저장
$PIPELINE &
PID=$!

# SIGINT (Ctrl+C)를 대기하고 처리하는 함수
trap "echo Stopping...; gst-launch-1.0 playbin uri=\"file:///dev/null\"; kill $PID; wait $PID; exit" SIGINT

# 파이프라인이 실행되는 동안 대기
wait $PID
