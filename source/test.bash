#!/bin/bash

export DISPLAY=:0
export LIBCAMERA_RPI_TUNING_FILE=/home/pi/Work/rc/imx219_175/imx219_160_v2.json

PIPELINE="gst-launch-1.0 libcamerasrc camera-name=\"/base/soc/i2c0mux/i2c@1/imx219@10\" ! video/x-raw, width=1600, height=1200, framerate=40/1 ! queue ! videoscale ! video/x-raw, width=640, height=480 ! videoconvert ! fpsdisplaysink video-sink=ximagesink sync=false text-overlay=true"


# 파이프라인 실행 및 백그라운드에서 실행되는 PID 저장
$PIPELINE &
PID=$!

# SIGINT (Ctrl+C)를 대기하고 처리하는 함수
trap "echo Stopping...; kill $PID; wait $PID; exit" SIGINT

# 파이프라인이 실행되는 동안 대기
wait $PID
