import pyautogui
import win32api
import win32con
# Define the coordinates of the screenshot
# Use PrintCoords.py to get the location of the save score button that pops up at the end of the game
save_r = (808, 775,1,1)
start_location = 843, 552
# x,y coordinates for the top left and bootm right of the game area
x1, y1, x2, y2 = 0, 350, 1690, 870


def click(point):
    x,y=point
    win32api.SetCursorPos(point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def scan():
    # Size of grid to check, some arbitray low numbers under
    width = 30
    height = 17
    original_coordinates = [(x, y) for x in range(width) for y in range(height)]

    # Target area, width and height of your game area
    target_width, target_height = x2 - x1,y2 - y1

    # Calculate scaling factors
    x_scale = target_width / width
    y_scale = target_height / height

    # Scale up the coordinates
    scaled_coordinates = [(int(x * x_scale), int(y * y_scale)) for x, y in original_coordinates]
    # Scan image
    p=0
    while True:
        save=pyautogui.screenshot(region=save_r)
        save_color=save.getpixel((0,0))
        if save_color == (255,209,84):
            return
        # Capture the screenshot
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        for i in range(len(scaled_coordinates)):
            x,y=scaled_coordinates[i]
            pixel_color = screenshot.getpixel((x,y))
            if pixel_color == (149,195,232):                #checking the grey area because its bigger
                point = x1+x,y1+y
                click(point)
                #pyautogui.moveRel(50, 0)
                break
            elif pixel_color == (255,209,84):
                return
        
        p+=1


click(start_location)
scan()
