from traceback import print_tb
from turtle import delay, goto
import pigpio
import time
import os, struct, array
from fcntl import ioctl

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
pi.set_PWM_frequency(MOTOR_PIN_A, PWM_FREQUENCY)  # PWM 주파수 설정
pi.set_PWM_frequency(MOTOR_PIN_B, PWM_FREQUENCY)  # 서보 모터의 PWM 주파수 설정
pi.set_PWM_dutycycle(MOTOR_PIN_A, MOTOR_DUTYCYCLE_A)  # 서보 모터의 PWM 듀티 사이클 설정
pi.set_PWM_dutycycle(MOTOR_PIN_B, MOTOR_DUTYCYCLE_B)  # 서보 모터의 PWM 듀티 사이클 설정
time.sleep(1)  # 1초 동안 지연
print("start")
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

def check_joystick_connection():
    try:
        fn = '/dev/input/js0'
        jsdev = open(fn, 'rb')
        return jsdev
    except:
        return None


def test_func():
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

try:
    while True:
        jsdev = check_joystick_connection()
        if jsdev:
            try:
                # 기존 코드 실행
                test_func()
                

                while True:
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
                print("조이스틱 연결 끊김")
                jsdev.close()
        # else:
        #     print("조이스틱 연결 없음. 재시도 중...")
        #     time.sleep(1)
finally:
    
    pi.write(SERVO_PIN_A, 0)
    pi.write(SERVO_PIN_B, 0)
    pi.set_PWM_dutycycle(MOTOR_PIN_A,0)
    pi.set_PWM_dutycycle(MOTOR_PIN_B,0)

    pi.stop()
    print("end_150")
    pi.set_PWM_dutycycle(LED_PIN, 150)  # PWM 듀티 사이클 설정
    #pi.set_PWM_dutycycle(SERVO_PIN, SERVO_DUTYCYCLE)  # 서보 모터의 PWM 듀티 사이클 설정
    time.sleep(1)  # 1초 동안 지연
