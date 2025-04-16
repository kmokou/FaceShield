import cv2
import numpy as np
import pyautogui
import keyboard
import time
from deepface import DeepFace
import ctypes
import sys
import win32gui
import win32con
import threading
import os
import warnings

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

def lock_workstation():
    try:
        ctypes.windll.user32.LockWorkStation()
        print("Workstation locked")
        sys.exit(0)
    except Exception as e:
        print(f"Lock error: {e}")
        sys.exit(1)

def blur_screen():
    try:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Apply heavy blur
        blurred_img = cv2.GaussianBlur(img, (99, 99), 30)
        
        # Create fullscreen window
        cv2.namedWindow('Screen Protection', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screen Protection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Screen Protection', blurred_img)
        cv2.waitKey(1)  # Needed to display the window
        
        # Bring to front and keep on top
        hwnd = win32gui.FindWindow(None, 'Screen Protection')
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return True
    except Exception as e:
        print(f"Blur error: {e}")
        return False

def main_loop():
    try:
        # Get absolute path to reference image
        ref_img_path = os.path.join(os.path.dirname(__file__), "ref.png")
        if not os.path.exists(ref_img_path):
            print(f"Error: Reference image not found at {ref_img_path}")
            return

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        blurred = False
        last_check = time.time()
        check_interval = 2  # Check every 2 seconds

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            current_time = time.time()
            if current_time - last_check >= check_interval:
                last_check = current_time
                try:
                    # Verify face against reference
                    result = DeepFace.verify(frame, ref_img_path, 
                                            enforce_detection=1,
                                            detector_backend='opencv')
                    
                    if not result['verified'] and not blurred:
                        print("Unauthorized face detected - blurring screen")
                        if blur_screen():
                            blurred = True
                            keyboard.block_key("windows")
                    elif result['verified'] and blurred:
                        print("Authorized face detected - restoring screen")
                        cv2.destroyAllWindows()
                        blurred = False
                        keyboard.unblock_key("windows")
                        
                except Exception as e:
                    print(f"Face verification error: {e}")
                    if not blurred:
                        if blur_screen():
                            blurred = True
                            keyboard.block_key("windows")

            # Check for quit key
            if cv2.waitKey(1) & 0xFF in [ord("q"), ord("й")]:
                print("Quitting...")
                break

    finally:
        # Cleanup
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        keyboard.unblock_key("windows")
        print("Resources released")

if __name__ == "__main__":
    print("Starting FaceShield protection...")
    main_thread = threading.Thread(target=main_loop, daemon=True)
    main_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)