import cv2 
import os
import HandModule as hm
import numpy as np
green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
purple = (255,0,255)
black = (0,0,0)
#size
eraser = 15
thickness = 30
color = blue

path = "C:/Yaser/Image paint"

tollbars = os.listdir(path)                    
toolbar = []
#--------------------------------------------
def coord(event , x , y , flag , param):
    if event ==  cv2.EVENT_LBUTTONDOWN:
        print(f' X = {int(x)} , Y = {int(y)}')
    
cv2.namedWindow("Painter")
cv2.setMouseCallback("Painter" , coord)    
#------------------------------------------
for toolpath in tollbars:
    image = cv2.imread(path + "/" + toolpath)
    toolbar.append(image)
menu = toolbar[0]
thicknessup = toolbar[5]
thicknessdown = toolbar[4]
thick = thicknessup
    
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720) 
detector = hm.Detector(detectionCon=1 , maxHands=1)
x0 , y0 = 0 , 0
blank = np.zeros((720,1280,3),np.uint8 )


while True:
    _ , frame = cap.read()
    
    frame = cv2.flip(frame , 1) 
    frame[0:125 ,0:1280] = menu
    frame[125:475 , 1130:1280] = thick
    frame = detector.findHands(frame)
    landmarklist = detector.Position(frame , draw=False)
    
    if len(landmarklist) !=0 :
        x1 , y1 = landmarklist[8][1] ,landmarklist[8][2]
        x2 , y2 = landmarklist[12][1] , landmarklist[12][2]
        fin_pos = detector.fing_up()
        
        if fin_pos[0] and fin_pos[1]:
            print("Selection")
            
            if y1 < 125 :
                if 250 < x1 < 450 :
                    color = blue
                    menu = toolbar[0]
                if 550 < x1 < 750 :
                    color = purple
                    menu = toolbar[1]
                if 800 < x1 < 950 :
                    color = green
                    menu = toolbar[2]
                if 1050 < x1 < 1200 :
                    color = black
                    menu = toolbar[3]
            cv2.rectangle(frame,(x1,y1-20) , (x2,y2+20) , color , -1)                    
        if fin_pos[0] and fin_pos[1] == False:
            print("Draw")
            
            if x0 == 0 and y0 == 0 :
                x0 , y0 = x1 , y1
            cv2.circle(frame , (x1, y1), 12 ,color , -7)
            if color == black:
                cv2.line(frame ,(x0,y0),(x1,y1), color , eraser)
                cv2.line(blank,(x0,y0),(x1,y1),color,eraser)
            else:
                cv2.line(frame ,(x0,y0),(x1,y1), color , thickness)
                cv2.line(blank,(x0,y0),(x1,y1),color,thickness)
                
                    
            cv2.line( frame , ( x0 , y0 ) , ( x1 , y1 ) , color ,12 )
            cv2.line( blank , ( x0 , y0 ) , ( x1 , y1 ) , color , 12 )
            x0 , y0 = x1 , y1
            
            
    Gray = cv2.cvtColor(blank , cv2.COLOR_BGR2GRAY)
    _ , Inv = cv2.threshold(Gray, 0, 255 , cv2.THRESH_BINARY_INV)
    Inv = cv2.cvtColor(Inv,cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame,Inv)
    frame = cv2.bitwise_or(frame , blank)       
             
    cv2.imshow("INVerse" , Inv)            
    cv2.imshow( "BLANK" , blank )
    cv2.imshow( "Painter" , frame )
    cv2.waitKey(1)
    
                             