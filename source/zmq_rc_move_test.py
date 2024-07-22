from dataclasses import asdict
import zmq
import json
import pigpio
import cv2
import numpy as np

import time
import os, struct, array
from fcntl import ioctl

# 초기 설정
pi = pigpio.pi()
MOTOR_PIN_A = 12
MOTOR_PIN_B = 13
SERVO_PIN_A = 10
SERVO_PIN_B = 11
PWM_FREQUENCY = 50
MOTOR_DUTYCYCLE_A = 0
MOTOR_DUTYCYCLE_B = 0
pi.set_mode(MOTOR_PIN_A, pigpio.OUTPUT)
pi.set_mode(MOTOR_PIN_B, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_A, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_B, pigpio.OUTPUT)
pi.set_PWM_frequency(MOTOR_PIN_A, PWM_FREQUENCY)
pi.set_PWM_frequency(MOTOR_PIN_B, PWM_FREQUENCY)
pi.set_PWM_dutycycle(MOTOR_PIN_A, MOTOR_DUTYCYCLE_A)
pi.set_PWM_dutycycle(MOTOR_PIN_B, MOTOR_DUTYCYCLE_B)

print("start")

# ZeroMQ 컨텍스트 생성
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5555")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

def draw_line(canvas, points, color):
    if len(points) > 1:
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], color, 2)

cv_x_left=206
cv_x_right=306
cv_y=230

# pi.set_PWM_dutycycle(MOTOR_PIN_A,0.33*255)
# pi.set_PWM_dutycycle(MOTOR_PIN_B,0)
try:
    while True:
        
        # 512x512 크기의 빈 이미지를 생성합니다.
        canvas = np.zeros((512, 512, 3), dtype="uint8")

        cv2.line(canvas, (cv_x_left,cv_y), (cv_x_left,512), (0, 255, 0), 2)
        cv2.line(canvas, (cv_x_right,cv_y), (cv_x_right,512), (0, 255, 0), 2)
        cv2.line(canvas, (cv_x_left,cv_y), (cv_x_right,cv_y), (0, 255, 0), 2)

        message = subscriber.recv()
        message_str = message.decode('utf-8')
        data = json.loads(message_str)

        sub_objects = data.get("HailoROI", {}).get("SubObjects", [])
        if len(sub_objects) > 0:
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 0)

        left_points = []
        right_points = []
        points = []

        for obj in sub_objects:
            detection = obj.get("HailoDetection", {})
            xmin = detection.get("HailoBBox", {}).get("xmin")
            ymin = detection.get("HailoBBox", {}).get("ymin")

            if (xmin * 512 > cv_x_left and ymin * 512 > cv_y) and (xmin * 512 < cv_x_right and ymin * 512 > cv_y) :
                
                if xmin * 512 < 256 : #left
                    cv2.circle(canvas, (int(xmin*512), int(ymin*512)), 5, (50, 0, 255),2)
                    left_points.append((int(xmin * 512), int(ymin * 512)))
                    
                elif xmin * 512 > 256 : #right
                    cv2.circle(canvas, (int(xmin*512), int(ymin*512)), 5, (200, 0, 255),2)
                    right_points.append((int(xmin * 512), int(ymin * 512)))
                    
            else :
                cv2.circle(canvas, (int(xmin*512), int(ymin*512)), 5, (255, 255, 0),2)

        if len(left_points)>0 and len(right_points)>0:
            left_points.sort(key=lambda x: (x[1], x[0]))
            right_points.sort(key=lambda x: (x[1], x[0]))
            if left_points[-1][1]>right_points[-1][1] :
                pi.write(SERVO_PIN_A, 1)
                pi.write(SERVO_PIN_B, 0)
            elif left_points[-1][1]<right_points[-1][1] :
                pi.write(SERVO_PIN_A, 0)
                pi.write(SERVO_PIN_B, 1)

        elif  len(left_points)>0:
            pi.write(SERVO_PIN_A, 1)
            pi.write(SERVO_PIN_B, 0)     
            
        elif  len(right_points)>0:
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 1)     
            
        else :
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 0)

        
        #cv2.imshow("Canvas", canvas)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        time.sleep(0.05)

finally:
    cv2.destroyAllWindows()
    pi.write(SERVO_PIN_A, 0)
    pi.write(SERVO_PIN_B, 0)
    pi.set_PWM_dutycycle(MOTOR_PIN_A,0)
    pi.set_PWM_dutycycle(MOTOR_PIN_B,0)

    pi.stop()