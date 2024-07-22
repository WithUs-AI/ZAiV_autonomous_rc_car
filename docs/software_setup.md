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