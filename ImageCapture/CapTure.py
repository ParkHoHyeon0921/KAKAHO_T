import os
import threading
import cv2
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

# 웹캠 열기
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미합니다. 다른 카메라를 사용하려면 인덱스를 조정하세요.

# 이미지 저장을 위한 변수 및 경로 설정
image_count = 0
make_folder_name = "../data/Image"  # 저장할 폴더 경로
output_path = make_folder_name + "/"  # 이미지를 저장할 폴더 경로를 지정하세요.
frame_rate = 10  # 캡처 속도 (프레임/초)
eye_status = "open"


def created_folder(directory):
    """
    :param directory: 생성하고싶은 폴더 경로
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        pass


def img_capture(eye_st):
    """
    :param eye_st:이미지 상태 or 이미지 이름
    :return:
    """
    created_folder(make_folder_name)
    image_count = 0
    while True:
        # 박스를 제외하고 캡처할 부분 선택
        ret, frame = cap.read()
        captured_frame = frame[y:y + height, x:x + width]
        image_filename = f"{output_path}{eye_st}_{image_count}.png"
        cv2.imwrite(image_filename, captured_frame)
        print(f"{eye_st} {image_count}")
        image_count += 1
        if image_count == 100:
            break

while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # 박스 좌표와 크기 정의 (여기서는 임의의 박스)
    x, y, width, height = 250, 150, 200, 250

    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)  # 초록색 사각형 그리기

    # 화면에 프레임 표시
    cv2.imshow("Webcam Capture", frame)
    # 박스 그리기


    # 이미지 캡처 (일정 간격으로 캡처)


    if cv2.waitKey(1) & 0xFF == ord('c'):
        img_thread = threading.Thread(target=img_capture, args=(eye_status, ))
        img_thread.start()
        if eye_status == "close":
            eye_status = "open"
        else:
            eye_status = "close"

    # 'q' 키를 누르거나 이미지 100장을 모두 촬영하면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()


