import subprocess
import pigpio
import os, struct, array
import signal
import time
import zmq
import json
import cv2
import numpy as np
from dataclasses import asdict
from datetime import datetime
from traceback import print_tb
from turtle import delay, goto
from fcntl import ioctl

###################################################################################
############################### GPIO Configurations ###############################
###################################################################################


pi = pigpio.pi()

# Motor & Servo
MOTOR_PIN_A = 12
MOTOR_PIN_B = 13
SERVO_PIN_A = 10
SERVO_PIN_B = 11
PWM_FREQUENCY = 50
MOTOR_DUTYCYCLE_A = 0
MOTOR_DUTYCYCLE_B = 0

# User Input & State led
GPIO_INPUT_BUTTON = 21
GPIO_INPUT_RUN_TYPE = 8 # Low = Recording, High = Inference
GPIO_OUTPUT_STATE_LED = 9


pi.set_mode(GPIO_INPUT_BUTTON, pigpio.INPUT)
pi.set_mode(GPIO_INPUT_RUN_TYPE, pigpio.INPUT)
pi.set_pull_up_down(GPIO_INPUT_RUN_TYPE, pigpio.PUD_DOWN)

pi.set_mode(GPIO_OUTPUT_STATE_LED, pigpio.OUTPUT)
pi.set_mode(MOTOR_PIN_A, pigpio.OUTPUT)
pi.set_mode(MOTOR_PIN_B, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_A, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_B, pigpio.OUTPUT)
pi.set_PWM_frequency(MOTOR_PIN_A, PWM_FREQUENCY)  # PWM 주파수 설정
pi.set_PWM_frequency(MOTOR_PIN_B, PWM_FREQUENCY)  # 서보 모터의 PWM 주파수 설정
pi.set_PWM_dutycycle(MOTOR_PIN_A, MOTOR_DUTYCYCLE_A)  # 서보 모터의 PWM 듀티 사이클 설정
pi.set_PWM_dutycycle(MOTOR_PIN_B, MOTOR_DUTYCYCLE_B)  # 서보 모터의 PWM 듀티 사이클 설정

print("GPIOs initialization complete.")
###################################################################################
################################ Process Variables ################################
###################################################################################
# Recording 프로세스를 저장할 변수
subprocess_record = None
subprocess_inference = None

pre_exec_commands = [
    "sudo modprobe hailo_pci",
    "export DISPLAY=:0",
    "export LIBCAMERA_RPI_TUNING_FILE=/home/pi/Work/rc/imx219_175/imx219_160_v2.json"
]

###################################################################################
################################ ZeroMQ Variables #################################
###################################################################################
# ZeroMQ 컨텍스트 생성
context = zmq.Context()
subscriber = context.socket(zmq.SUB)  # 구독자 소켓 생성
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # 모든 메시지를 구독

previous_connection_check_time = time.time()

###################################################################################
################################ Driving Variables ################################
###################################################################################
# 기준 영역 좌표 설정
cv_x_left = 206  # 왼쪽 기준 x 좌표
cv_x_right = 306  # 오른쪽 기준 x 좌표
cv_y = 230  # y 좌표

###################################################################################
################################ Joystick Variables ###############################
###################################################################################
time.sleep(1)  # 1초 동안 지연

print("Show Joystick Input Devices")
for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
axis_states = {}
# 버튼 값 저장 변수
button_states = {}

axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []
jsdev = None

###################################################################################
##################################### Functions ###################################
###################################################################################
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command execution successfull: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute: {command}\n: {e}")

def kill_gstreamer_processes():
    try:
        # Find gstreamer process id by 'pgrep' command.
        gstreamer_processes = subprocess.check_output(['pgrep', '-f', 'gst-launch-1.0'])

        # Make a list composite of line formatted.
        process_ids = gstreamer_processes.decode('utf-8').strip().split('\n')

        for pid in process_ids:
            pid = int(pid)  # string to int
            os.kill(pid, signal.SIGTERM)  # Send signal process kill
            print(f"Killed GStreamer {pid} process.")

    except subprocess.CalledProcessError:
        print("There is no gstreamer process")
    except Exception as e:
        print(f"Exception: {e}")

def check_joystick_connection():
    try:
        fn = '/dev/input/js0'
        jsdev = open(fn, 'rb')
        return jsdev
    except:
        return None


def init_joystick_by_hid_descriptor():
    buf = array.array('B', [0] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
    js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
    print('Device name: %s' % js_name)
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
    # x,y 축이면 2
    num_axes = buf[0]
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
    # 버튼이 두 개면 2
    num_buttons = buf[0]
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP
    # 읽은 값에서 총 축 수만큼 loop 돌림
    for axis in buf[:num_axes]:
        axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
        axis_map.append(axis_name)
        # 해당 축 0.0 으로 초기화
        axis_states[axis_name] = 0.0
    buf = array.array('H', [0] * 200)
    ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

    for btn in buf[:num_buttons]:
        btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
        button_map.append(btn_name)
        button_states[btn_name] = 0

def process_js_manual_control():
    global jsdev
    if jsdev == None:
        jsdev = check_joystick_connection()
        if jsdev:
            init_joystick_by_hid_descriptor()
    if jsdev:
        try:
            evbuf = jsdev.read(8)
            # 기존 코드 처리
            time, value, type, number = struct.unpack('IhBB', evbuf)

            # type이 0x80이면 장치 초기 상태이다.
            if type & 0x80:
                print("(initial)", end="")

            if type & 0x01:
                # number 값으로 해당 버튼 이름 가져오기
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        print("%s pressed" % (button))
                        if button == "y":
                            pi.write(SERVO_PIN_A, 0)
                            pi.write(SERVO_PIN_B, 1)
                        elif button == "a":
                            pi.write(SERVO_PIN_A, 1)
                            pi.write(SERVO_PIN_B, 0)

                    else:
                        print("%s released" % (button))

                        pi.write(SERVO_PIN_A, 0)
                        pi.write(SERVO_PIN_B, 0)


            if type & 0x02:
                # number로 해당 축의 이름 가져오기
                axis = axis_map[number]
                if axis:
                    fvalue = value / 32767.0
                    # 상태값(0, 1, -1)을 저장
                    axis_states[axis] = fvalue
                    print("%s: %.3f" % (axis, fvalue))
                    print(axis)
                    if axis=='y':

                        if fvalue < 0:
                            pi.set_PWM_dutycycle(MOTOR_PIN_A,(fvalue*-255)/3)
                            pi.set_PWM_dutycycle(MOTOR_PIN_B,0)
                            print("front =",(fvalue*-255)/3)
                        elif fvalue > 0:
                            pi.set_PWM_dutycycle(MOTOR_PIN_A,0)
                            pi.set_PWM_dutycycle(MOTOR_PIN_B,(fvalue*255)/3)
                            print("back =",(fvalue*255)/3)
                        else :
                            pi.set_PWM_dutycycle(MOTOR_PIN_A,0)
                            pi.set_PWM_dutycycle(MOTOR_PIN_B,0)

        except:
            print("Closed Joystick Connection")
            jsdev.close()
            jsdev = None

# 함수: 구독자 소켓 연결
def connect_socket():
    global subscriber
    try:
        subscriber.connect("tcp://localhost:5555")  # 지정된 주소로 서버에 연결
    except Exception as e:
        print(f"Exception of connect socket: {e}")

# 연결 상태 확인 함수
def check_connection():
    global subscriber
    try:
        # 연결 상태를 점검하기 위해 빈 메시지를 보내고 확인
        subscriber.send(b'', zmq.NOBLOCK)
        # 응답을 기다립니다 (타임아웃 설정)
        subscriber.recv(zmq.NOBLOCK)
        return True
    except zmq.Again:
        return False
    except Exception as e:
        print(f"Exception of check connection : {e}")
        return False

# 라인을 그리는 opencv 함수 정의
def draw_line(canvas, points, color):
    if len(points) > 1:
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], color, 2)

def process_js_auto_control():
    global previous_connection_check_time
    global subscriber
    if subscriber:
        # 33%의 듀티 사이클로 rc카 전진
        pi.set_PWM_dutycycle(MOTOR_PIN_A, 0.33 * 255)
        pi.set_PWM_dutycycle(MOTOR_PIN_B, 0)
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
        cv2.waitKey(1)
        #if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        #    break
        #time.sleep(0.05)  # 50ms 대기
    else:
        current_time = time.time()
        # 2 초마다 체크하는 것으로 설정.
        if current_time - previous_connection_check_time >= 2:
            pi.set_PWM_dutycycle(MOTOR_PIN_A, 0)
            pi.set_PWM_dutycycle(MOTOR_PIN_B, 0)
            print("Try to connect...")
            subscriber.close()  # 기존 소켓 닫기
            time.sleep(0.2)  # 잠시 대기 후 재연결 시도
            connect_socket()  # 재연결 시도
            previous_connection_check_time = current_time


def process_record(bRecord = False):
    global subprocess_record
    if bRecord == 1:
        # Run GStreamer
        now = datetime.now()
        f_path = 'location=./' + now.strftime('%Y%m%d_%H%M%S') + '.mp4'

        subprocess_record = subprocess.Popen([
            'gst-launch-1.0', '-v',
            'libcamerasrc', 'camera-name=/base/soc/i2c0mux/i2c@1/imx219@10',
            '!', 'video/x-raw, width=1600, height=1200, framerate=40/1',
            '!', 'videoscale',
            '!', 'video/x-raw, width=640, height=480',
            '!', 'videoconvert',
            '!', 'queue',
            '!', 'x264enc',
            '!', 'mp4mux', 'fragment-duration=100',
            '!', 'filesink', f_path
        ])

        print("Run record subprocess")
    else:
        if subprocess_record != None:
            subprocess_record.terminate()
            subprocess_record = None
            time.sleep(0.5)
            print("Terminate record subprocess")
        kill_gstreamer_processes()

def process_inference(bInference = False):
    global subprocess_inference
    if bInference == 1:
        # Run GStreamer
        subprocess_inference = subprocess.Popen([
            'gst-launch-1.0', '-v',
            'libcamerasrc', 'camera-name=/base/soc/i2c0mux/i2c@1/imx219@10',
            '!', 'video/x-raw, width=1600, height=1200, framerate=41/1',
            '!', 'queue',
            '!', 'videoscale',
            '!', 'video/x-raw, width=640, height=480',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'videoscale', 'n-threads=2',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'videoconvert', 'n-threads=3',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'hailonet', 'hef-path=/home/pi/Work/rc/imx219_175/config/rc_hose_300.hef', 'batch-size=1',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'hailofilter', 'function-name=yolov5', 'config-path=/home/pi/Work/rc/imx219_175/config/yolov5_rc_hose.json',
            'so-path=/home/pi/Work/rc/imx219_175/config/libyolo_post.so', 'qos=false',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'hailooverlay',
            '!', 'hailoexportzmq',
            '!', 'queue', 'max-size-buffers=5', 'max-size-bytes=0', 'max-size-time=0',
            '!', 'videoconvert', 'n-threads=3',
            '!', 'fpsdisplaysink', 'video-sink=ximagesink', 'name=hailo_display', 'sync=false', 'text-overlay=true'
        ])

        time.sleep(3)
        connect_socket()

        print("Run inference subprocess")
    else:
        if subprocess_inference != None:
            subprocess_inference.terminate()
            subprocess_inference = None
            time.sleep(0.5)
            print("Terminate inference subprocess")
            cv2.destroyAllWindows()  # OpenCV 윈도우 닫기

        kill_gstreamer_processes()

###################################################################################
###################################### Loops ######################################
###################################################################################
try:
    kill_gstreamer_processes()
    for cmd in pre_exec_commands:
        run_command(cmd)

    while True:

        if pi.read(GPIO_INPUT_BUTTON) == 0:
            if pi.read(GPIO_INPUT_RUN_TYPE) == 0:

                if subprocess_inference != None:
                    print('Running inference process. Will be terminate')
                    process_inference(False)

                if subprocess_record == None:
                    print('Record process is None')
                    process_record(True)
                    if pi.read(GPIO_OUTPUT_STATE_LED) == 0:
                        pi.write(GPIO_OUTPUT_STATE_LED, 1)
                else:
                    print('Running record process. Will be terminate')
                    process_record(False)
                    if pi.read(GPIO_OUTPUT_STATE_LED) == 1:
                        pi.write(GPIO_OUTPUT_STATE_LED, 0)
            else:
                if subprocess_record != None:
                    print('Running record process. Will be terminate')
                    process_record(False)

                if subprocess_inference == None:
                    print('Inference process is None')
                    process_inference(True)
                    if pi.read(GPIO_OUTPUT_STATE_LED) == 0:
                        pi.write(GPIO_OUTPUT_STATE_LED, 1)
                else:
                    print('Running inference process. Will be terminate')
                    process_inference(False)
                    if pi.read(GPIO_OUTPUT_STATE_LED) == 1:
                        pi.write(GPIO_OUTPUT_STATE_LED, 0)
            time.sleep(1)

        if subprocess_record == None:
            if jsdev != None:
                jsdev.close()
                jsdev = None
        if pi.read(GPIO_INPUT_RUN_TYPE) == 0: # Run type - Record
            if subprocess_record != None:
                process_js_manual_control()
        else: # Run type - Inference
            if subprocess_inference != None:
                process_js_auto_control()

        # 상태 체크 간격
        #time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    process_record(False)
    process_inference(False)

    cv2.destroyAllWindows()  # OpenCV 윈도우 닫기

    if pi.read(GPIO_OUTPUT_STATE_LED) == 1:
        pi.write(GPIO_OUTPUT_STATE_LED, 0)

    # 조향을 직진으로 설정
    pi.write(SERVO_PIN_A, 0)
    pi.write(SERVO_PIN_B, 0)
    # 직진 모터 동작 정지
    pi.set_PWM_dutycycle(MOTOR_PIN_A, 0)
    pi.set_PWM_dutycycle(MOTOR_PIN_B, 0)

    pi.stop()# GPIO 설정 초기화
    if jsdev != None:
        jsdev.close()

    if subscriber:
        subscriber.close()
    if context:
        context.term()
