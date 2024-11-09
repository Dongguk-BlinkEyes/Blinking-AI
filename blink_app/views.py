import cv2
import dlib
import time
from django.http import StreamingHttpResponse
from django.shortcuts import render  # 추가
from scipy.spatial import distance

# dlib 얼굴 탐지기 및 랜드마크 예측 모델 초기화
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("blink_app/shape_predictor_68_face_landmarks.dat")

EAR_THRESHOLD = 0.20
CONSEC_FRAMES = 1

# 눈 깜빡임을 감지하는 함수
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def blink_detection():
    cap = cv2.VideoCapture(0)
    blink_count = 0
    frame_count = 0
    start_time = time.time()  # 시간 초기화

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        # 경과 시간 계산
        elapsed_time = time.time() - start_time
        
        for face in faces:
            shape = predictor(gray, face)
            landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
            
            left_eye = landmarks[42:48]
            right_eye = landmarks[36:42]
            
            left_EAR = eye_aspect_ratio(left_eye)
            right_EAR = eye_aspect_ratio(right_eye)
            
            ear = (left_EAR + right_EAR) / 2.0
            
            if ear < EAR_THRESHOLD:
                frame_count += 1
            else:
                if frame_count >= CONSEC_FRAMES:
                    blink_count += 1
                    start_time = time.time()
                frame_count = 0

            cv2.putText(frame, f"Blinks: {blink_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Time: {elapsed_time:.2f}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

# 스트리밍 화면을 제공하는 뷰
def video_feed(request):
    return StreamingHttpResponse(blink_detection(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# index 뷰 함수 (기본 HTML 페이지 렌더링)
def index(request):
    return render(request, 'blink_app/index.html')
