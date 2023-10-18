import pyautogui
from PIL import ImageGrab
import time

x, y = 500, 500
#make this any pixel inside the color changing area
#use PrintCoords.py if you need to find the coordinates

pyautogui.click(x, y)
screenshot = pyautogui.screenshot(region=(x, y, x + 1, y + 1))
o_color = screenshot.getpixel((0, 0))
count=1
while True:
    new_color = pyautogui.screenshot(region=(x, y, x + 1, y + 1))
    if new_color != (206,38,54):
        pyautogui.click()
        time.sleep(1)
        if count==5:
            break
        pyautogui.click()
        count+=1
        
