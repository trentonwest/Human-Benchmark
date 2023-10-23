import pyautogui
import time
import win32api
import win32con

point = 500, 500
#make this any pixel inside the color changing area
#use PrintCoords.py if you need to find the coordinates

def click(point):
    x,y=point
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


pyautogui.click(point)
x,y=point
count=1
while True:
    new_color = pyautogui.pixel(x,y)
    if new_color[1] >= 200:
        click(point)
        time.sleep(1)
        if count==5:
            break
        click(point)
        count+=1
        
