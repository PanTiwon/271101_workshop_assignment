import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time
from pyfirmata import Arduino, SERVO

time.sleep(1.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
video = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

tipIds = [4, 8, 12, 16, 20]

def check_user_input(input):
        try:
                int(input)
                return True
        except ValueError:
                try:
                        float(input)
                        return True
                except ValueError:
                        return False

def rotateservo(pin, angle):
        board.digital[pin].write(angle)
        time.sleep(0.015)

def servo(total,pin):#creat condition to controll servo
    if (total)==0:
            rotateservo(pin,0)
    elif (total)==1:
            rotateservo(pin,18)
    elif (total)==2:
            rotateservo(pin,36)
    elif (total)==3:
            rotateservo(pin,52)
    elif (total)==4:
            rotateservo(pin,72)
    elif (total)==5:
            rotateservo(pin,90)
    elif (total)==6:
            rotateservo(pin,108)
    elif (total)==7:
            rotateservo(pin,126)
    elif (total)==8:
            rotateservo(pin,144)
    elif (total)==9:
            rotateservo(pin,162)
    elif (total)==10:
            rotateservo(pin,180)

def main():
        print("_____________________________________")
        cport = input()
        print("'Enter the camera port: \n'")
        while not check_user_input(cport):
                print('Please enter a number not string')
                cport = input('Enter the camera port: ')

        comport = input('Enter the arduino board COM port: ')
        while not check_user_input(comport):
                print('Please enter a number not string')
                comport = input('Enter the arduino board COM port: ')

        global board
        try:
                board = Arduino('COM' + comport)
        except Exception as e:
                print(f"Error connecting to Arduino: {e}")
                return

        pin = 9
        board.digital[pin].mode = SERVO

        video = cv2.VideoCapture(int(cport))
        if not video.isOpened():
                print("Error opening video stream or file")
                return

        with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                try:
                        while True:
                                success, img = video.read()
                                if not success:
                                        print("Failed to capture image")
                                        break

                                hands_detected, img = detector.findHands(img)

                                # คำนวณจำนวนรวมของนิ้วที่ชูขึ้น
                                total_fingers = 0
                                if hands_detected:
                                        # ตรวจสอบมือแรก
                                        hand1 = hands_detected[0]
                                        fingers1 = detector.fingersUp(hand1)
                                        total_fingers += fingers1.count(1)

                                        # ตรวจสอบมือที่สอง (ถ้ามี)
                                        if len(hands_detected) == 2:
                                                hand2 = hands_detected[1]
                                                fingers2 = detector.fingersUp(hand2)
                                                total_fingers += fingers2.count(1)

                                # ควบคุมเซอร์โวมอเตอร์
                                servo(total_fingers, pin)

                                # แสดงผลภาพ
                                cv2.putText(img, "Tidtawan Shingkorn 670610760: ", (100, 70), cv2.FONT_HERSHEY_PLAIN, 2., (0, 255, 255), 1)
                                cv2.putText(img, "Count fingers: "+str(total_fingers), (200, 400), cv2.FONT_HERSHEY_PLAIN, 2., (0, 255, 0), 1)
                                cv2.putText(img, "Servo Degree: "+str(total_fingers*18), (200, 450), cv2.FONT_HERSHEY_PLAIN, 2., (0, 255, 0), 1)
                                cv2.imshow("Image", img)
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                        break
                except Exception as e:
                        print(f"An error occurred: {e}")
                finally:
                        video.release()
                        cv2.destroyAllWindows()

if __name__ == "__main__":
        main()
