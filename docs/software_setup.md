# Software Setup Guides

## OS Setup


1. Install
1.1. Download SD Writing Tools
* https://www.raspberrypi.com/software/로 이동한 호스트 OS에 따라 Raspberry Pi Imager를 다운로드하고 설치합니다.


1.2. Download EMMC Writing Tools
* https://github.com/raspberrypi/usbboot/raw/master/win32/rpiboot_setup.exe로 이동한 다음 rpiboot_setup.exe를 다운로드하여 설치합니다.
* https://win32diskimager.org/로 이동한 다음 win32diskimager를 다운로드하고 설치합니다.

Writing을 위해서는 USB Type-C 케이블이 필요합니다.

1.3. Download image
* ​모델에 따라 이미지를 선택합니다.
* Raspberry Pi CM4 (Recommended "No EMMC", included Wi-Fi): 

* Download
* (Account: pi/hello)
* Raspberry Pi 4B (included Wi-Fi): 

* Download
* (Account: pi/hello)
* Raspberry Pi CM4 (DIY AI CCTV Image): 

* Download
* (Account: pi/hello)


2. Write
2.1. SD Card Writing
* microSD 카드를  microSD Writer에 장착한 후 PC에 삽입합니다. (USB 3.0 권장)
* 설치된 Raspberry Pi Imager를 실행합니다.
* 실행된 Raspberry Pi Imager에서 "OS 선택"을 클릭합니다.
* "Use custom"을 선택하세요.
* 제공된 이미지를 선택하세요.
* "Choose SD Card" 클릭합니다.
* 첨부된 SD 카드 드라이브를 클릭하세요.
* "쓰기"를 클릭하세요. (경고 메시지가 나타나면 "예"를 클릭하여 진행하세요)
* 쓰기 및 확인 과정은 SD Card Writer에 따라 다를 수 있으며, USB3.0을 사용하는 경우 약 5분 정도 소요됩니다.
* 완료
* 완료 후 마이크로 SD 카드를 라즈베리 파이에 삽입하세요.

## Bash files
1. gst_pipe.bash
    >cam, mp4의 detection 결과를 hailoexportzmq을 사용하여 zmq 결과를 보내주는 .bash

    > 처음실행시 cam, mp4 터미널에서 선택가능

2. recode.bash
    >cam 화면을 녹화하는 gstreamer .bash

3. test.bash
    >cam 화면을 ximagesink을 이용하여 비디오 테스트하는 gstreamer .bash

4. test_dc_rc_car_ya.py
    >rc car를 조종하는 .py

    >실행시 먼저 ap모드 연결 후 192.168.50.1의 gamepad 실행필요

5. zmq_rc_move_test.py
    >gst_pipe.bash에서 보낸 zmq 결과를 받은 후 파싱하여 opnecv imshow로 출력 후 rc car를 동작시키는 자율주행 .py
