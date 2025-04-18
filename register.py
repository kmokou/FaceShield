import cv2
import numpy as np
from deepface import DeepFace
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 255, 0)
thickness = 2
line_type = 2

def check_face(image_path):
    try:
        result = DeepFace.analyze(image_path, enforce_detection=True)
        return bool(result)
    except Exception as e:
        print(f"Face detection failed: {e}")
        return False

print("Нажмите 'c' для регистрации лица. Нажмите 'q', чтобы выйти")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Ошибка: не удалось сохранить изображение")
        break

    clean_frame = frame.copy()

    cv2.putText(frame, "Press 'c' to capture the face", (30, 40),
                font, font_scale, font_color, thickness, line_type)

    cv2.imshow('Face Registration', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Выход...")
        break

    if key == ord('c'):
        image_path = os.path.join(script_dir, "captured_face.png")
        ref_path = os.path.join(script_dir, "ref.png")

        cv2.imwrite(image_path, clean_frame)

        if check_face("captured_face.png"):
            print("Лицо обнаружено! Сохранено как ref.png.")
            if os.path.exists(ref_path):
                os.remove(ref_path)
            os.rename(image_path, ref_path)
            break
        else:
            print("No face detected. Try again.")
            cv2.putText(frame, "Лицо не обнаружено", (30, 80),
                        font, 0.5, (0, 0, 255), thickness, line_type)
            cv2.imshow('Регистрация лица', frame)
            cv2.waitKey(1500)

cap.release()
cv2.destroyAllWindows()
