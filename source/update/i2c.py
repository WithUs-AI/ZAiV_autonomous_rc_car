import os
import re
import json
import random
import subprocess
import RPi_I2C_driver
import RPi.GPIO as GPIO

from time import *

def wlan_scan():
    result_ifconfig = subprocess.run(['ifconfig', 'wlan0'], capture_output=True, text=True)
    result_iwconfig = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
    
    tmp = re.search(r'ESSID:"([^"]+)"', result_iwconfig.stdout)
    tmp2 = re.search(r'inet ([\d.]+)', result_ifconfig.stdout)
    if tmp:
        ssid = tmp.group(1)
    else:
        ssid = False
    if tmp2:
        ip = tmp2.group(1)
    else:
        ip = False
    return ssid, ip

def eth0_scan():
    result_ifconfig = subprocess.run(['ifconfig', 'eth0'], capture_output=True, text=True)
    ip_match = re.search(r'inet ([\d.]+)', result_ifconfig.stdout)
    if ip_match:
        ip = ip_match.group(1)
        return ip
    else:
        return None

def scroll_text(text, line):
    for i in range(len(text)):
        if i == len(text) - 15:
            break
        lcd.lcd_display_string(" " * 16, line)
        lcd.lcd_display_string(text[i:], line)
        sleep(0.5)
        #lcd.lcd_display_string(" " * len(text), 2)
    sleep(1)

def lcd_clear():
    lcd.lcd_display_string(" " * 16, 1)
    lcd.lcd_display_string(" " * 16, 2)

def ReadPin():
    pin_number = 40
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    tmp = GPIO.input(pin_number)
    GPIO.cleanup()
    return tmp
    
def print_eth0():
    ip = eth0_scan()
    lcd_clear()
    
    if ip:
        print("eth0 :", ip)
        lcd.lcd_display_string("eth0", 1)
        lcd.lcd_display_string(ip, 2)
    else:
        print("연결된 eth0를 찾을 수 없습니다.")
        lcd.lcd_display_string("eth0 error", 1)
    
def lcd_print_wlan01(ssid, ip):
    print(ssid, ":" ,ip)
    
    lcd.lcd_display_string(ip, 2)
    if len(ssid) + 2 > 15:
        scroll_text( "W:" + ssid, 1)
    lcd.lcd_display_string("W:" + ssid, 1)

def lcd_print_wlan02(ssid, ip):
    print(ssid, ":" ,ip)
    
    lcd.lcd_display_string(ip, 2)
    if len(ssid) + 2 > 15:
        scroll_text( "A:" + ssid, 1)
    lcd.lcd_display_string("A:" + ssid, 1)

def print_ssid_lines():
    file_path = "/etc/hostapd/hostapd.conf"
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("ssid="):
                ssid_value = line.strip()[5:]  # ssid= 다음의 값을 저장
                return ssid_value
    return None
    
def change_ssid(new_ssid):
    file_path = "/etc/hostapd/hostapd.conf"
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            if line.startswith("ssid="):
                line = f"ssid={new_ssid}\n"
            file.write(line)
            
def print_wlan0():
    ssid, ip = wlan_scan()
    lcd_clear()
    
    if ip == '192.168.50.1':
        ssid = print_ssid_lines()
        lcd_print_wlan02(ssid, ip)
    elif ip and ssid != False:
        lcd_print_wlan01(ssid, ip)
    else:
        print("연결된 wlan0를 찾을 수 없습니다.")
        lcd.lcd_display_string("wlan0 error", 1)

def check_dhcpcd_config():
    content = """

interface wlan0
static ip_address=192.168.50.1/24
nohook wpa_supplicant"""
    
    with open(dhcpcdFile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() == "static ip_address=192.168.50.1/24":
                return True
            elif line.strip() == "#static ip_address=192.168.50.1/24":
                return True
                
    with open(dhcpcdFile, 'a') as file:
        file.write(content)
    
    return False
    
def APmod(state):
    ssid, ip = wlan_scan()
    print(check_dhcpcd_config())
    
    if state:
        if APssid == print_ssid_lines():
            with open(dhcpcdFile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() == "static ip_address=192.168.50.1/24":
                        return True
        
        print("APmod on")
        change_ssid(APssid)
        subprocess.run(['sudo', 'sed', '-i', 's/^#static ip_address=192.168.50.1\/24/static ip_address=192.168.50.1\/24/', dhcpcdFile])
        subprocess.run(['sudo', 'sed', '-i', 's/^#nohook wpa_supplicant/nohook wpa_supplicant/', dhcpcdFile])
        subprocess.run(['sudo', 'reboot'])
        
    # elif state == False and ip == '192.168.50.1':
    #     print("APmod off")
    #     subprocess.run(['sudo', 'sed', '-i', 's/^static ip_address=192.168.50.1\/24/#static ip_address=192.168.50.1\/24/', dhcpcdFile])
    #     subprocess.run(['sudo', 'sed', '-i', 's/^nohook wpa_supplicant/#nohook wpa_supplicant/', dhcpcdFile])
    #     subprocess.run(['sudo', 'reboot'])

def read_json(file_path):
    if not os.path.exists(file_path):
        print("APmod on")
        random_number = random.randint(100000, 999999)
        ssid = "ZAiV_autonomous_rc_car_" + str(random_number)
        
        # JSON 데이터 생성
        data = {
            "AP": {
                "ssid": ssid
            }
        }

        # JSON 파일 생성
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"JSON 파일 '{file_path}'이 생성되었습니다.")
            
    with open(file_path, "r") as file:
        json_data = json.load(file)
        ssid = json_data["AP"]["ssid"]
    
    if not ssid:
        print("APmod on")
        random_number = random.randint(100000, 999999)
        ssid = "ZAiV_autonomous_rc_car_" + str(random_number)
        with open(file_path, "r") as file:
            json_data = json.load(file)

        json_data["AP"]["ssid"] = ssid

        # 수정된 JSON 파일 저장
        with open(file_path, "w") as file:
            json.dump(json_data, file, indent=4)
            
    return ssid
    

dhcpcdFile = '/etc/dhcpcd.conf'
ap_config_json_path = "/home/pi/i2c-lcd-and-ap-mod-control/ap_config.json"

i2c_check = False

try:
    lcd = RPi_I2C_driver.lcd(0x27)
    i2c_check = True
except IOError:
    print("I2C 연결 오류: 0x27 주소에 I2C가 연결되어 있지 않습니다.")

if i2c_check == True:
    lcd.noCursor()
    
APssid = read_json(ap_config_json_path)


APmod(True)