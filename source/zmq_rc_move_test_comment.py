from dataclasses import asdict
import zmq
import json
import pigpio
import cv2
import numpy as np
import time
import os, struct, array
from fcntl import ioctl


pi = pigpio.pi()  # pigpio 라이브러리를 사용하여 Raspberry Pi GPIO 핀을 제어하기 위한 인스턴스 생성
MOTOR_PIN_A = 12  # 전진 모터 A 제어 핀
MOTOR_PIN_B = 13  # 전진 모터 B 제어 핀
SERVO_PIN_A = 10  # 조향 모터 A 제어 핀
SERVO_PIN_B = 11  # 조향 모터 B 제어 핀
PWM_FREQUENCY = 50  # PWM 주파수 설정
MOTOR_DUTYCYCLE_A = 0  # 전진 모터 A의 초기 듀티 사이클
MOTOR_DUTYCYCLE_B = 0  # 전진 모터 B의 초기 듀티 사이클

# GPIO 핀의 모드 설정
pi.set_mode(MOTOR_PIN_A, pigpio.OUTPUT)
pi.set_mode(MOTOR_PIN_B, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_A, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_B, pigpio.OUTPUT)

# PWM 주파수 및 듀티 사이클 설정
pi.set_PWM_frequency(MOTOR_PIN_A, PWM_FREQUENCY)  # 모터 A의 PWM 주파수 설정
pi.set_PWM_frequency(MOTOR_PIN_B, PWM_FREQUENCY)  # 모터 B의 PWM 주파수 설정
pi.set_PWM_dutycycle(MOTOR_PIN_A, MOTOR_DUTYCYCLE_A)  # 모터 A의 듀티 사이클 설정
pi.set_PWM_dutycycle(MOTOR_PIN_B, MOTOR_DUTYCYCLE_B)  # 모터 B의 듀티 사이클 설정

print("start")  # 프로그램 시작 메시지 출력

# ZeroMQ 컨텍스트 생성 및 구독자 설정
context = zmq.Context()  # ZeroMQ 컨텍스트 생성
subscriber = context.socket(zmq.SUB)  # 구독자 소켓 생성
subscriber.connect("tcp://localhost:5555")  # 지정된 주소로 서버에 연결
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # 모든 메시지를 구독

# 라인을 그리는 opencv 함수 정의
def draw_line(canvas, points, color):
    if len(points) > 1:
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], color, 2)

# 기준 영역 좌표 설정
cv_x_left = 206  # 왼쪽 기준 x 좌표
cv_x_right = 306  # 오른쪽 기준 x 좌표
cv_y = 230  # y 좌표

# 33%의 듀티 사이클로 rc카 전진
pi.set_PWM_dutycycle(MOTOR_PIN_A, 0.33 * 255)
pi.set_PWM_dutycycle(MOTOR_PIN_B, 0)

try:
    while True:
        
        # 512x512 크기의 opencv 캔버스 생성
        canvas = np.zeros((512, 512, 3), dtype="uint8")

        # opencv로 기준 선 그리기
        cv2.line(canvas, (cv_x_left, cv_y), (cv_x_left, 512), (0, 255, 0), 2)  # 왼쪽 선
        cv2.line(canvas, (cv_x_right, cv_y), (cv_x_right, 512), (0, 255, 0), 2)  # 오른쪽 선
        cv2.line(canvas, (cv_x_left, cv_y), (cv_x_right, cv_y), (0, 255, 0), 2)  # 수평 기준선

        message = subscriber.recv()  # zmq 메시지 수신
        message_str = message.decode('utf-8')  # 바이트 문자열을 UTF-8로 디코딩
        data = json.loads(message_str)  # JSON 문자열을 파이썬 객체로 변환

        sub_objects = data.get("HailoROI", {}).get("SubObjects", [])  # HailoROI의 SubObjects를 sub_objects로 전달
        if len(sub_objects) > 0:  # sub_objects가 있을 경우 조향을 직진으로
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 0)

        left_points = []  # 왼쪽 포인트 저장 리스트
        right_points = []  # 오른쪽 포인트 저장 리스트

        # sub_objects에서 detection 객체의 좌표를 가져옴
        for obj in sub_objects:
            detection = obj.get("HailoDetection", {})  # detection된 객체의 정보 가져오기
            xmin = detection.get("HailoBBox", {}).get("xmin")  # 바운딩 박스 중간의 x 좌표값을 xmin으로
            ymin = detection.get("HailoBBox", {}).get("ymin")  # 바운딩 박스 중간의 y 좌표값을 ymin으로

            # 바운딩 박스가 기준 영역 내에 있는지 확인
            if (xmin * 512 > cv_x_left and ymin * 512 > cv_y) and (xmin * 512 < cv_x_right and ymin * 512 > cv_y):
                
                if xmin * 512 < 256:  # 왼쪽 영역일 경우
                    cv2.circle(canvas, (int(xmin * 512), int(ymin * 512)), 5, (50, 0, 255), 2)  # 왼쪽 포인트 원으로 표시
                    left_points.append((int(xmin * 512), int(ymin * 512)))  # 왼쪽 포인트 리스트에 추가
                    
                elif xmin * 512 > 256:  # 오른쪽 영역일 경우
                    cv2.circle(canvas, (int(xmin * 512), int(ymin * 512)), 5, (200, 0, 255), 2)  # 오른쪽 포인트 원으로 표시
                    right_points.append((int(xmin * 512), int(ymin * 512)))  # 오른쪽 포인트 리스트에 추가
                    
            else:  # 기준 영역 밖의 객체인 경우
                cv2.circle(canvas, (int(xmin * 512), int(ymin * 512)), 5, (255, 255, 0), 2)  # 다른 색으로 표시

        # 왼쪽과 오른쪽 포인트가 모두 있을 경우
        if len(left_points) > 0 and len(right_points) > 0:
            left_points.sort(key=lambda x: (x[1], x[0]))  # 왼쪽 포인트를 y 좌표 기준으로 정렬
            right_points.sort(key=lambda x: (x[1], x[0]))  # 오른쪽 포인트를 y 좌표 기준으로 정렬
            
            # 가장 높은 y 값을 가진 포인트 비교하여 조향모터 제어
            if left_points[-1][1] > right_points[-1][1]:  # 왼쪽 포인트 y값이 더 높을 경우 좌회전
                pi.write(SERVO_PIN_A, 1)
                pi.write(SERVO_PIN_B, 0)
            elif left_points[-1][1] < right_points[-1][1]:  # 오른쪽 포인트 y값이 더 높을 경우 우회전
                pi.write(SERVO_PIN_A, 0)
                pi.write(SERVO_PIN_B, 1)

        # 왼쪽 포인트만 있을 경우 좌회전
        elif len(left_points) > 0:
            pi.write(SERVO_PIN_A, 1)
            pi.write(SERVO_PIN_B, 0)
            
        # 오른쪽 포인트만 있을 경우 우회전
        elif len(right_points) > 0:
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 1)
            
        # 포인트가 없을 경우 직진
        else:
            pi.write(SERVO_PIN_A, 0)
            pi.write(SERVO_PIN_B, 0)

        # 캔버스에 그려진 이미지 표시
        cv2.imshow("Canvas", canvas)  # OpenCV 윈도우에 캔버스 이미지 표시
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
            break
        #time.sleep(0.05)  # 50ms 대기

finally:
    # 루프 종료 후 정리 작업
    cv2.destroyAllWindows()  # OpenCV 윈도우 닫기
    # 조향을 직진으로 설정
    pi.write(SERVO_PIN_A, 0)
    pi.write(SERVO_PIN_B, 0)    
    # 직진 모터 동작 정지
    pi.set_PWM_dutycycle(MOTOR_PIN_A, 0)
    pi.set_PWM_dutycycle(MOTOR_PIN_B, 0)

    pi.stop()  # pigpio 인스턴스 종료

