![waving](https://capsule-render.vercel.app/api?type=waving&color=FF6666&height=300&section=header&text=All-in-one%20Apple%20Box&fontcolor=FFFFCC&fontSize=70&animation=fadeIn&&fontAlignY=30&desc=Capstone%20Project&descAlignY=51&descAlign=80)
## 목차
- 📝 [프로젝트 소개](#프로젝트-소개)
    - [배경 및 필요성](#배경-및-필요성)
- 🛠 [구현기능](#구현기능)
- 🔍 [이미지 분석](#이미지-분석🔍)
    - [사과 이미지 수집](#사과-이미지-수집)
    - [데이터 라벨링](#데이터-라벨링)
    - [데이터 학습](#데이터-학습)
    - [객체 검출](#객체-검출)
    - [컨베이어 연동](#컨베이어-연동)
    - [실행](#실행)
- 🎬[작동영상 및 작품사진](#작동영상-및-작품사진🎬)
- ✨ [업데이트](#-업데이트)
<br  />
<br />
<br />





## 프로젝트 소개📝
#### 배경 및 필요성
- 사과는 전체 과수작물 중 생산량 1위
- 농업 종사자 근골격계 질환 발생율 증가 추세
- 선별 공정에서의 시간과 비용 소모 多
<br />

## 구현기능🛠
#### 1. 팔받침대
    - 30 - 60대의 어깨너비, 팔 길이 고려하여 사이즈 선정 후 모델링
    - 작업 중 팔을 받침으로써 어깨 부하 감소
#### 2.  [이미지 분석](#이미지-분석🔍)
    - Jetson Nano에서 Yolov5 구동하여 실시간 객체 검출
    - 사과 외관을 기준으로 정과와 흠과 분류
#### 3.  높이조절 리프트
    - 실린더를 통해 높이조절
    - 리모컨 기능
    - 작업자에 따라 높이 조절하여 허리부하 감소
    - 트럭 적재함으로 손쉽게 이동 가능
<br />

## 이미지 분석🔍
#### - 사과 이미지 수집
> 정과: [AI허브](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=149)를 통해 정과 데이터 확보<br>
품종, 크기별 약 600장<br>

>흠과: 흠과 직접 구매 후 촬영 셋 조성하여 촬영<br>
각도별 약 300장<br>
<img src="https://user-images.githubusercontent.com/115714519/212478669-6718804e-4684-46bb-9574-42db09d5d0e4.png" width="300" height="200">


#### - 데이터 라벨링
> 1. [Roboflow](https://app.roboflow.com/ml0930)를 통해 **Good apple** 과 **damaged apple**로 라벨링 진행<br />
>2. Flip과 Rotation으로 데이터 추가 확보<br>
<img src="https://user-images.githubusercontent.com/115714519/212479027-8c9ac66e-cbc8-44b0-b08a-3203f51c19ea.png" width="300" height="150">


#### - 데이터 학습
> **Googol colab**을 통해 머신러닝 실행
```
#roboflow에서 만든 데이터셋 불러오기
!curl -L "https://app.roboflow.com/ds/sr3XcWrSo1?key=kmhDDEWnYv" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip 

#Yolov5 불러오기
!git clone https://github.com/ultralytics/yolov5.git 

#이미지를 텍스트 파일로 변환
from glob import glob
train_img_list = glob('/content/train/images/*.jpg')
val_img_list = glob('/content/valid/images/*.jpg')

with open('/content/train.txt', 'w') as f:
  f.write('\n'.join(train_img_list) + '\n')

with open ('/content/valid.txt', 'w') as f:
  f.write('\n'.join(val_img_list) + '\n') 

#이미지크기 416x416, batch:16, epochs:1000으로 학습 실행
!python /content/yolov5/train.py --img 416 --batch 16 --epochs 1000 --data /content/data.yaml --weights yolov5s.pt --name yolov5_apple --cfg /content/yolov5/models/yolov5s.yaml
#412번째에서 오버피팅으로 인해 학습종료
```


#### - 객체 검출
>**Jetson Nano**에서 학습파일 다운로드<br>
**OpenCV** 및 **Pytorch**설치 ([Jetson Nano 환경구현](https://whiteknight3672.tistory.com/category/Works/DeepLearning) 참고)<br>
**Yolov5**실행<br>
<img src="https://user-images.githubusercontent.com/115714519/212479929-afc7a034-fc30-4c87-b86a-1532aa164540.png" width="400" height="200" >


#### - 컨베이어 연동
>Jetson Nano의 **GPIO제어**를 통해 신호 입출력<br>
객체가 **Good apple**이고 정확도 0.3 이상일 경우 **정방향** 제어<br>
**damaged apple**이고 정확도 0.3 이상일 경우 **역방향** 제어
<img src="https://user-images.githubusercontent.com/115714519/212481426-f20dfbd3-2846-41a9-860f-df384e1ddbdc.png">

```

# set pin numbers to the board's
ENA = 33
IN1 = 35
IN2 = 37
GPIO.setmode(GPIO.BOARD)

# initialize EnA, In1 and In2
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

#컨베이어 제어 함수
def forward():
    time.sleep(3.5)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(7)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

def backward():
    time.sleep(2)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(7)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

#검출객체별 스레드 실행 코드
                        if names[c] == 'damegd apple' and accNum > 0.30:
                            print(names[c] + ': ' + f'{conf:.2f}')
                            thread = threading.Thread(target=forward)
                            thread.start()
                            thread.join()
                        elif names[c] == 'Good apple' and accNum > 0.30:
                            print(names[c] + ': ' + f'{conf:.2f}')
                            thread = threading.Thread(target=backward)
                            thread.start()

```
<br />

#### 실행
> 1.Jetson Nano 부팅<br>
> 2.터미널 실행<br>
> 3.cd yolov5 #yolov5 디렉터리로 이동<br>
> 4.python detect2.py --weights C://hgjt/Desktop/yolov5/runs/train/yolov5_apple2/weights/best.pt --source 0 <br>
#커스텀 학습파일인 best.pt로 detect2 파일 실행


## 작동영상 및 작품사진🎬
<img src="https://user-images.githubusercontent.com/115714519/212467233-b179148f-90e5-4796-b640-1b7d8dbcb41a.jpg" width="150" height="150"><img src="https://user-images.githubusercontent.com/115714519/212467551-c8d501c5-fd0d-4868-bf3c-e0657a00d00f.jpg" width="150" height="150">
<br >
<img src="https://user-images.githubusercontent.com/115714519/212481914-cf289ab8-cd6c-42e7-ba01-4baac5d0c2ff.jpg" width="300" height="200">
<br>
<img src="https://user-images.githubusercontent.com/115714519/212482057-359a9a3f-52ab-4285-9fe7-79e18bb9d658.jpg" width="300" height="200">

<br>

[![선별 작동 영상](http://img.youtube.com/vi/JcInwGUPN_M/0.jpg)](https://www.youtube.com/watch?v=JcInwGUPN_M) 
<br />

## 업데이트✨