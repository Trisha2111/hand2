import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller
import pyautogui
import imutils
import numpy as np

keyboard=Controller()
wcam,hcam=720,620
cam = cv2.VideoCapture(0)
cam.set(3,wcam)
cam.set(4,hcam)
mpdrawing=mp.solutions.drawing_utils
mphand=mp.solutions.hands

hands=mphand.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)
tipid=[4,8,12,16,20]
width=int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height=int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
state=None
def countfingers(img,landmark,handNo=0):
    global state
    if landmark:
        lm=landmark[handNo].landmark
        fingers=[]
        for i in tipid:
            fingertip=lm[i].y
            fingerbottom=lm[i-2].y
            thumbtip=lm[i].x
            thumbbottom=lm[i-2].x
            if i !=4:
                if fingertip<fingerbottom:
                    fingers.append(1)
                    print("Finger with id ",i," is open")
                if fingertip>fingerbottom:
                    fingers.append(0)
                    print("Finger with id ",i," is closed" )
            else:
                if thumbtip<thumbbottom:
                    fingers.append(1)
                    print("Finger with id ",i," is open")
                if thumbtip>thumbbottom:
                    fingers.append(0)
                    print("Finger with id ",i," is closed" )


        totalfingers=fingers.count(1)
        cv2.putText(img,f"Fingers:{totalfingers}",(50,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,255),2)

        if totalfingers==5:
            state="play"
        if totalfingers==0 and state=="play":
            state="pause"
            keyboard.press(Key.space)
        fingertipx=(lm[8].x)*width
        if totalfingers==1:
            if fingertipx<width-400:
                keyboard.press(Key.left)
            if fingertipx>width-150:
                keyboard.press(Key.right)

def drawhandlandmarks(img,landmark):
    if landmark:
        for i in landmark:
            mpdrawing.draw_landmarks(img,i,mphand.HAND_CONNECTIONS)

while True:
    success, image = cam.read()
    image=cv2.flip(image,1)
    results=hands.process(image)
    handlandmark=results.multi_hand_landmarks
    drawhandlandmarks(image,handlandmark)
    countfingers(image,handlandmark)
    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()

