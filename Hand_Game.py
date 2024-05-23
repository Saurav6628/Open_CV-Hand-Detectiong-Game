# Importing all used pacakges
import cv2
import mediapipe as mp
import numpy as np
import random as rd
import time

# Creating Colors
red=(0,0,255)
green=(0,255,0)
blue=(255,0,0)
yellow=(0,255,255)
white=(255,153,153)
orange=(153,204,255)
cyan=(255,255,153)
purple=(255,153,204)
grey=(244,244,244)
black=(0,0,0)

# Creating extra functions
# If number is between any 2 numbers
def between(x,val,key="9"):
    if x>boxes[key][3][0][val]:
        if x<boxes[key][3][1][val]:
            return True
        else:
            return False
    else:
        return False

# Printing the box is grabed or not
def grabed(x,y):
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in keys:
        if between(x,0,i) and between(y,1,i):
            print(i)


# Functions for grabbing and swaing the blocks
def grabedn(x,y,swapkey="9"):
    if between(x,0,swapkey) & between(y,1,swapkey):
            return True
    return False


def swap(x,y,boxes,swapkey="9"):
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for key1 in keys:
        if between(x,0,key1) & between(y,1,key1):
            if key1!=swapkey:
                boxes[key1][0],boxes[swapkey][0],boxes[key1][2],boxes[swapkey][2]=boxes[swapkey][0],boxes[key1][0],boxes[swapkey][2],boxes[key1][2]
                return boxes,key1
    return boxes,swapkey

# Calculating difference between fingers
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


# Drawing boxes
def drawback(background):
    keys=["1","2","3","4","5","6","7","8","9"]
    for key in keys:
        cv2.rectangle(background,boxes[key][1],(boxes[key][1][0]+140,boxes[key][1][1]+140),boxes[key][2],-1)
        cv2.putText(background, boxes[key][0], (boxes[key][1][0] + 60, boxes[key][1][1] + 65), 0,1,black,2)



# drawing circle on hands
def draw(img,landmarks,color=(0,255,0)):
    if landmarks:
        for handlm in landmarks:
            x1,y1,x2,y2=0,0,0,0
            h, w, c = img.shape
            for id, lm in enumerate(handlm.landmark):
                if id == 8:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    x1,y1=cx,cy
                    cv2.circle(img, (cx, cy), 5, color, -1)
                elif id == 12:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    x2,y2 = cx, cy
                    xn,yn=(x1 + x2) // 2, (y1 + y2) // 2
                    cv2.circle(img, (cx, cy), 5, color, -1)
                    cv2.circle(img, (xn,yn), 5, red, -1)
                    return img,xn,yn,distance(x1,y1,x2,y2)
                else:
                    None

    return img,False,False,False


# Checking something
def check(box):
    keys=["1","2","3","4","5","6","7","8","9"]
    c=1
    for key in keys:
        if key==box[key][0]:
            c+=1
        else:
            break
    return c==9

# Generating random values and putting those values inside a list called values
values=[]
while len(values)!=8:
    x=rd.randint(1,8)
    if str(x) not in values:
        values.append(str(x))

# Creating data for boxes
boxes={"7":[values[0],(0,280),red,((0,280),(0+140,280+140))],"3":[values[1],(280,0),green,((280,0),(280+140,0+140))],
       "6":[values[2],(280,140),blue,((280,140),(280+140,140+140))],"1":[values[3],(0,0),yellow,((0,0),(0+140,0+140))],
       "8":[values[4],(140,280),white,((140,280),(140+140,280+140))],"4":[values[5],(0,140),orange,((0,140),(0+140,140+140))],
       "2":[values[6],(140,0),cyan,((140,0),(140+140,0+140))],"5":[values[7],(140,140),purple,((140,140),(140+140,140+140))],
       "9":["",(280,280),grey,((280,280),(280+140,280+140))]}



# Creating a white a background
background=np.zeros((420,420,3),"uint8")
background[:]=(255,255,255)

swkey="9"
Count=0

# creating inbuilt hand detection model
mphands=mp.solutions.hands
hands=mphands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)
grab=False

cap=cv2.VideoCapture(0)
print("Let Start the Game")
time1=time.time()

while True:

    ret,img=cap.read()
    results = hands.process(img)
    results = results.multi_hand_landmarks
    img,x,y,dis=draw(img,results)

    drawback(background)
    if x:
        if dis<30:
            cv2.circle(background, (x, y), 5, (0,0,102), -1)
            if grab==False and grabedn(x,y,swkey):
                print("Grabbed")
                grab=True
        else:
            if grab==True:
                print("Released")
                Count+=1
                boxes,swkey=swap(x,y,boxes,swkey)
                keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                print([[key, boxes[key][0]] for key in keys])
                grab=False
            cv2.circle(background,(x,y),5,black,-1)
    t=check(boxes)
    cv2.imshow("Hand",img)
    cv2.imshow("Game",background)
    key=cv2.waitKey(1)
    # q to quit the game
    if key==ord("q"):
        break
    elif key==ord("p"):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        print([[key,boxes[key][0]] for key in keys])
    elif t:
        time2=time.time()
        time2=time2-time1
        print("Game Is Finished")
        print("Time Take:",time2,"sec")
        print("Moves take:",Count)
        break
cap.release()
cv2.destroyAllWindows()