import cv2, os, time
from functools import reduce
import numpy as np
from PIL import Image
import uuid

from sanityRequest import includeSanity
from sms import makeSms
from request import sendImage

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

last_frame = None
last_mov_frame = None
start_timer = 0

lastTime = 0
saved_photo = True
delayTimer = 0
photoMs = 500
resetMs = 5 * 1000
resetTimer = 0

minX = 0
minW = 0
minY = 0
minH = 0

greenSquare = {"y": frame_height - 200, "h": 200, "color": (0, 255, 0)}
purpleSquare = {"y": frame_height - 300, "h": 100, "color": (255, 0, 255)}
idkSquare = {"y": frame_height - 400, "h": 100, "color": (255, 255, 0)}
squares = [greenSquare, purpleSquare, idkSquare]

sensibilidade = 10000 # 1000   #quanto menor mais sensivel (detecta movimento menores)

def somarArray(array):
    num = reduce(lambda x, y: x + y, array)
    return num

def current_milli_time():
    return round(time.time() * 1000)
def most_common_used_color(img):
    width, height = img.size
    r_total = 0
    g_total = 0
    b_total = 0
 
    count = 0
 
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (r_total/count, g_total/count, b_total/count)

while True:
    ret, frame = cam.read()
    out.write(frame)

    _, frame = cam.read()
    frame_copy = frame.copy()  
    if last_frame is None:
        last_frame = frame  
    else:
        diff = cv2.absdiff(last_frame, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=4)                        
        contours, hirarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if start_timer == 1 and current_milli_time() > lastTime:
            saved_photo = False
            start_timer = -1
        
        if saved_photo == False:
            cv2.imwrite("frame.png", frame)
            
            #cv2.imwrite("framecut.jpg", last_mov_frame[y:y+h, x:x+w])
            cv2.imwrite("framecut.png", last_mov_frame[minY:minY+minH, minX:minX+minW])
            saved_photo = True
            print("============ FOTO TIRADA ============ ")

            print("ENVIANDO FOTO")
            print("FOTO ENVIADA COM SUCESSO")
            includeSanity("frame.png")
            # sendImage("frame.png")
            makeSms("Movimento detectado...")

            resetTimer = current_milli_time() + resetMs
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # cv2.imshow('thresh', thresh)
        # cv2.imshow('dilated', dilated)

        for contour in contours:
                curSquare = greenSquare
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) > sensibilidade:
                    last_mov_frame = frame.copy()

                    if start_timer == 0:
                        minX = x
                        minW = w
                        minY = y
                        minH = h
                        lastTime = current_milli_time() + photoMs

                    if start_timer == 1:
                        if x < minX: minX = x
                        if w > minW: minW = w
                        if (y > curSquare["y"] and y-h < curSquare["y"] + curSquare["h"]) and y < minY: minY = y
                        if h > minH: minH = h

                    if saved_photo:
                        if y+h > curSquare["y"] and y < curSquare["y"] + curSquare["h"]:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                            if start_timer == 0: start_timer = 1
                        else:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    if minY < curSquare["y"]:
                        minY = curSquare["y"]
                        minH += (minY - curSquare["y"])
        
        if start_timer == 1 and minX != None: cv2.rectangle(frame, (minX, minY), (minX+minW, minY+minH), (255, 0, 0), 2)

        #for square in squares:
            #cv2.rectangle(frame, (0, square["y"]), (frame_width, square["y"]+square["h"]), square["color"], 2)
        
        if resetTimer != 0 and current_milli_time() > resetTimer:
            resetTimer = 0
            start_timer = 0
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break            
        last_frame = frame_copy

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
out.release()
cv2.destroyAllWindows()
os.remove("output.mp4")