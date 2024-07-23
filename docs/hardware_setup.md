# Hardware Setup

이 페이지에는 ZAiV RC CAR의 구성에 필요한 hardware setup이 있습니다. hardware setup이 끝난 후 [software setup](./software_setup.md)을 따라하세요.

## Tools

* 십자 드라이버

## Step 1 - Rc Car 분해 및 기본 세팅
### Step 1-1 - Rc Car 외피 제거

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60310435-c165b600-9907-11e9-858b-238e801b11abw.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60310436-c165b600-9907-11e9-88d1-fd009d01w5eda.png" height=128/>
<img src="https://user-images.githubusercwontent.com/25759564/60310437-c1fe4c80-9907-11e9-8862-f0249a61c680.png" height=128/>
<img src="https://user-images.githubusercwontent.com/25759564/60310439-c1fe4c80-9907-11e9-8495-990fa6ae926e.png" height=128/>

1. Rc Car의 전방에서 4개의 핀을 뽑습니다.

2. 십자 드라이버를 사용하여 Rc Car의 후방에서 볼트 2개를 제거합니다.

3. 고정이 해제된 Rc Car의 외피를 제거합니다.

### Step 1-2 - Rc Car 상판 제거

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311224-37b7e780-990b-11e9-92b1-04fd1bcs78bw41.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311225-37b7e780-990b-11e9-9738-aab32effafws32.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311226-37b7e780-990b-11e9-9454-9f54187a61wsaf.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311228-38507e00-990b-11e9-9bb5-53256784eaws85.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311229-38507e00-990b-11e9-890b-3123dcdf4csewa.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311231-38507e00-990b-11e9-832d-fdb3b6w96fs336.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311233-38e91480-990b-11e9-86be-5b01f8e4a9d2.JwPG" height=128/>
<img src="https://user-images.githubusercontenwt.com/25759564/60311234-38e91480-990b-11e9-9277-3f71895a40c7.wpng" height=128/>

1. 위 사진에 표시되어 있는 볼트를 총 6개 제거합니다. 이 때 중간의 볼드 2개는 Step 2-5에서 사용함으로 따로 보관합니다.

### Step 1-3 - 기존 통신보드 제거

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311869-ec530880-990d-11e9-9b9b-efabfcef251ㅈe.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311871-eceb9f00-990d-11e9-9786-bc463f637dㅈ74.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311872-eceb9f00-990d-11e9-8770-3021aa6b11ㅈb3.png" height=128/>
<img src="https://user-images.githubusercontㅈent.com/25759564/60311873-eceb9f00-990d-11e9-9872-cae74856b125.png" height=128/>

1. 사진의 보드에 연결되어 있는 전선을 니퍼나 가위도 잘라 제거합니다.
> 전선은 아래의 Step 3 에서 사용하므로 최대한 길게 잘라 주십시오.

2. 전선을 제거한 보드를 십자드라이버를 이용하여 Rc Car에서 제거합니다.

### Step 1-4 - 배터리 단자 납땜

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311869-ec530880-990d-11e9-9b9b-efabfcef251ㅈe.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311871-eceb9f00-990d-11e9-9786-bc463f637dㅈ74.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311872-eceb9f00-990d-11e9-8770-3021aa6b11ㅈb3.png" height=128/>
<img src="https://user-images.githubusercontㅈent.com/25759564/60311873-eceb9f00-990d-11e9-9872-cae74856b125.png" height=128/>

1. 기존의 배터리 단자를 제거하고 사용하려는 배터리에 맞는 단자를 납땜하여 줍니다.
> +는 빨간색, -는 검정색으로 구분합니다.

### Step 1-5 - DC 5v 강하모듈 케이블 납땜

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311869-ec530880-990d-11e9-9b9b-efabfcef251ㅈe.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311871-eceb9f00-990d-11e9-9786-bc463f637dㅈ74.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311872-eceb9f00-990d-11e9-8770-3021aa6b11ㅈb3.png" height=128/>
<img src="https://user-images.githubusercontㅈent.com/25759564/60311873-eceb9f00-990d-11e9-9872-cae74856b125.png" height=128/>

1. DC 5v 강하모듈과 ZAiV-AHPm 전원 커넥터를 out방향에 사진과 같이 납땜합니다.

2. 여분의 전선을 이용하여 in방향에 사진과 같이 납땜합니다.
> +는 빨간색, -는 검정색으로 구분합니다.

3. 쇼트 방지를 위하여 수축튜브나 절연테이프로 절연처리를 합니다.

### Step 1-6 - ZAiV-m.2, cm4 방열판 장착

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311869-ec530880-990d-11e9-9b9b-efabfcef251ㅈe.png" height=128/>

1. 사진을 참고하여 ZAiV-m.2와 cm4에 방열판을 장착합니다.

## Step 2 - hardware 조립
### Step 2-1 - 카메라 브라켓과 댐퍼 플레이트 결합

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60311869-ec530880-990d-11e9-9b9b-efabfcef251ㅈe.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311871-eceb9f00-990d-11e9-9786-bc463f637dㅈ74.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60311872-eceb9f00-990d-11e9-8770-3021aa6b11ㅈb3.png" height=128/>
<img src="https://user-images.githubusercontㅈent.com/25759564/60311873-eceb9f00-990d-11e9-9872-cae74856b125.png" height=128/>

1. M2x8mm 스틸 볼트너트 2개를 사용하여 카메라 브라켓과 댐퍼 플레이트를 결합합니다.

### Step 2-2 - 댐퍼 플레이트와 베이스 플레이트 결합

<a></a>
<img src="https://user-images.githubusercontㅈent.com/25759564/60312424-23c2b480-9910-11e9-824e-7fb36213dd65.png" height=128/>
<img src="https://user-images.githubuserconㅈtent.com/25759564/60312425-23c2b480-9910-11e9-94af-ccc7b5d9f07a.png" height=128/>
<img src="https://user-images.githubuserconㅈtent.com/25759564/60312427-245b4b00-9910-11e9-8781-ba4ec20c0012.png" height=128/>
<img src="https://user-images.githubuseㅈrcontent.com/25759564/60312429-245b4b00-9910-11e9-84d5-f3ccf10fcf86.png" height=128/>
<img src="https://user-images.githubusercㅈontent.com/25759564/60312430-245b4b00-9910-11e9-8244-22c40b3b5851.png" height=128/>
<img src="https://user-images.githubusercontㅈent.com/25759564/60312431-245b4b00-9910-11e9-8a6d-f6f1ae954ab2.png" height=128/>


1. 베이스 플레이트에 댐퍼를 결합합니다. 
    > 댐퍼를 결합시에는 댐퍼가 찢어지지 않도록 날카로운 도구는 사용을 금합니다. 

2. 베이스 플레이트에 결합된 댐퍼를 댐퍼 플레이트와 결합합니다.

3. 마지막으로 댐퍼와 함께 제공된 고정핀을 체결합니다.

### Step 2-3 - cm4와 cm4 Wi-Fi 안테나 결합

<a></a>
<img src="https://user-images.githubusercontㅈent.com/25759564/60312424-23c2b480-9910-11e9-824e-7fb36213dd65.png" height=128/>

1. cm4와 cm4 Wi-Fi 안테나를 사진과 같이 결합합니다.

### Step 2-4 - cm4와 베이스 플레이트 결합

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60313003-4d7cdb00-9912-11e9-98cb-5890120a7949.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313004-4d7cdb00-9912-11e9-90bd-2fbe3bee0a05.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313006-4d7cdb00-9912-11e9-86a9-bbc0dc62b94f.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313007-4d7cdb00-9912-11e9-84e3-03944f236987.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313008-4d7cdb00-9912-11e9-9894-eac89f324822.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313009-4e157180-9912-11e9-984a-afbf62bbb15d.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313010-4e157180-9912-11e9-858c-6a463433f53f.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60313012-4e157180-9912-11e9-9743-5647a3c5599b.png" height=128/>

1. CM4의 방향에 주의하여 베이스 플레이트의 지정된 자리에 놓습니다.

2. 제공된 나일론 볼트 너트로 각 모서리 4군데를 체결합니다. 이때 볼트의 방향을 사진과 동일하게 체결합니다.

### Step 2-5 - 모터 드라이버와 베이스 플레이트 결합

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60314883-1bbb4280-9919-11e9-9f76-c561c9de9cb2.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60314885-1bbb4280-9919-11e9-8eb2-5c1f97b6b6dc.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60314884-1bbb4280-9919-11e9-8c4f-d43a5441fbe7.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60314887-1c53d900-9919-11e9-9d48-3770831164c8.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60314888-1c53d900-9919-11e9-8c84-4a91f0e727af.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60314889-1c53d900-9919-11e9-97aa-9015e4e94aca.png" height=128/>

1. 모터 드라이버의 방향에 주의하여 베이스 플레이트의 지정된 자리에 놓습니다.

2. 제공된 나일론 볼트 너트로 각 모서리 4군데를 체결합니다.

### Step 2-6 - Rc Car와 차대 연결 부품 결합

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60316400-2d074d80-991f-11e9-8f4c-49cbf84b3fb8.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60316401-2d074d80-991f-11e9-8f3b-82714cfef58f.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60316392-2c6eb700-991f-11e9-89cc-3f9babc37a17.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60316393-2c6eb700-991f-11e9-94e5-4ebe4b2582fd.png" height=128/>

1. 차대 연결 부품의 구멍에 나일론 너트 2개를 끼워 넣습니다.

2. 차대 연결 부품을 나일론 너트가 빠지지 않도록 주의 하면서 사진처럼 Rc Car의 중간 부분에 위치 시킵니다.

3. Step 1-2에서 Rc Car의 상판을 제거할때 나온 볼트 2개를 이용하여 조립합니다.

4. M2.5x20mm 나일론 서포트 2개를 사진처럼 결합합니다.

### Step 2-7 - RC Car와 베이스 플레이트 결합

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60316395-2d074d80-991f-11e9-80dc-63c819b76963.png" height=128/>
<img src="https://user-images.githubusercontent.com/25759564/60316445-5627de00-991f-11e9-8408-35b9c1fec8da.png" height=128/>

1. 베이스 플레이트의 앞쪽의 홀과 Rc Car의 앞쪽의 Rc Car의 외피가 고정되어 있던 부분에 끼워 장착합니다.

2. 끼워서 장착 후 Rc Car의 외피를 고정시켰던 핀을 다시 장착하여 고정합니다.

3. 베이스 플레이트의 중간에 뚤려있는 2개의 홀과 앞서 Step 2-5에서 장착한 M2.5x20mm 나일론 서포트에 나일론 볼트 2개를 이용하여 고정합니다.

### Step 2-8 - cm4 Wi-Fi 안테나 고정

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. cm4 Wi-Fi 안테나를 사진과 같이 M2.5x20mm 나일론 서포트 부위에 케이블타이로 고정합니다.

### Step 2-9 - ZAiV-AHPm 장착 및 ZAiV-m.2 고정 브라켓 장착

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. ZAiV-m.2를 고정하기 위하여 M2.5x5mm 나일론 서포트와 M2.5x5mm 나일론 볼트를 이용하여 사진과 같이 고정합니다.

2. ZAiV-AHPm를 사진을 참고하여 방향에 맞게 cm4에 장착합니다.

### Step 2-10 - 카메라 장착

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 사진과 같이 카메라와 카메라 케이블을 장착합니다.

2. 카메라를 카메라 브라켓에 M2x8mm 스틸 볼트너트 2개를 이용하여 고정시킵니다.

3. 카메라 케이블을 사진을 참고하여 방향에 맞춰 장착합니다.

### Step 2-11 - ZAiV-m.2 장착

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 사진을 참고하여 ZAiV-m.2를 ZAiV-AHPm의 m.2 슬롯에 장착 후 M2.5x5mm 나일론 너트를 이용하여 고정시킵니다.

## Step 3 - 케이블 연결
### Step 3-1 - 모터 케이블 연결

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 사진을 참고하여 색상에 주의하여 앞, 뒤 모터 케이블 을 모터 드라이버에 장착합니다.


### Step 3-2 - 전원 케이블, DC 5v 강하모듈 케이블 연결

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 사진을 참고하여 스위치에서 나온 빨간색 케이블(+)과 DC 5v 강하모듈의 in+ 케이블을 모터 드라이버의 12v에 십자드라이버를 이용하여 고정합니다.

2. 사진을 참고하여 배터리 케이블에서 나온 검정색 케이블(-)과 DC 5v 강하모듈의 in- 케이블을 모터 드라이버의 GND에 십자드라이버를 이용하여 고정합니다.

### Step 3-3 - ZAiV-AHPm 전원 커넥터 및 점퍼 케이블 연결

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 사진을 참고하여 DC 5v 강하모듈 out 부분에 연결된 ZAiV-AHPm 전원 커넥터를 ZAiV-AHPm에 연결합니다.

2. 사진을 참고하여 ZAiV-AHPm과 모터 드라이버를 점퍼 케이블로 연결합니다.

### Step 3-4 - 배터리 체커기 연결방법

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60317621-bcfbc600-9924-11e9-9cb5-af886100dd48.png" height=128/>

1. 배터리의 하얀색 커넥터의 검은색 라인에 배터리 체커기의 가장 왼쪽 단자를 기준으로 연결합니다.

2. 비프음이 두번 울린뒤 배터리의 전체 전압, 1셀 전압, 2셀 전압 순으로 표시됩니다.
전체 전압이 7.5v 이하가 되면 충전이 필요합니다.

## Hardware setup complete!

<a></a>
<img src="https://user-images.githubusercontent.com/25759564/60377764-33a0ce00-99ce-11e9-8aa4-688d0a05dc01.png" height=256/>

## Next

[software setup](./software_setup.md)을 따라하세요.
