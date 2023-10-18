import pyautogui
from PIL import Image
import math
import pytesseract
import re

# Path to the Tesseract executable (you need to install Tesseract on your system)
# You only need this if tesseract isnt in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Use PrintCoords.py to find the coordinates
# x1 y1 is the top left coordinate of the area where the boxes appear
# x2 y2 is the bottom right coordinate of the area where the boxes appear, very close to the edge of the screen
x1,y1,x2,y2=23, 222, 1700, 800

# Location of the continue button
continue_location=840, 716

feild=(x1,y1,x2-x1,y2-y1)

def calculate_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def filter_points(points, distance_threshold=10):
    filtered_points = []
    while len(points) > 0:
        current_point = points.pop(0)
        filtered_points.append(current_point)
        points = [point for point in points if calculate_distance(current_point, point) > distance_threshold]
    return filtered_points

def get_white_list():
    screenshot = pyautogui.screenshot(region=feild)

    # Define grid parameters
    #how many pixels we want to sample to find the numbers
    grid_size = 200
    pixel_size = screenshot.width // grid_size 

    # List to store coordinates of white pixels
    white_pixels = []

    # Draw dots on the image for checked positions and find white pixels
    # Uncomment this and the commented section below the double for loop
    #draw = ImageDraw.Draw(screenshot)

    for row in range(grid_size):
        for col in range(grid_size):
            # Get the pixel color at the center of the grid cell
            x = col * pixel_size + pixel_size // 2
            y = row * pixel_size + pixel_size // 2
            if x>screenshot.width:
                x=screenshot.width -5
            if y>screenshot.height:
                y=screenshot.height -5
            pixel_color = screenshot.getpixel((x, y))

            # Check if the pixel is white (255, 255, 255)
            #print(pixel_color)
            if pixel_color[0]>200 and pixel_color[1]>200 and pixel_color[2]>200:
                # Add the coordinates of white pixel to the list
                white_pixels.append((x, y))


    filtered=filter_points(white_pixels, distance_threshold=60)

    # This will show you all the white pixels that we use to find the actual numbers later
    #for pin in filtered:
    #    x,y=pin
    #    draw.ellipse([(x - 2, y - 2), (x + 2, y + 2)], fill='blue')
    #screenshot.save('dotted.png')

    return filtered

#_________________________________________________________________
#gets list of white pixels to look at later^^^^^^^^^^^^^^^^^^^
#_________________________________________________________________

def run_stage():
    filtered=get_white_list()
    count=1
    final_list=[]
    padded_image = Image.new("RGB", (400,400), color=(116,116,116))

    debug=''#input(Debug this stage?)
    for pin in filtered:
        x,y=pin
        x+=x1
        y+=y1

        num_box=(x-50,y-30,100,110)
        screenshot=pyautogui.screenshot(region=num_box).convert("L")

        position = ((400 - screenshot.width) // 2, (400 - screenshot.height) // 2)
        padded_image.paste(screenshot, position)

        text = pytesseract.image_to_string(padded_image,config='--psm 6 -l eng')
        text=text.replace("\n", "")

        #print(text)
        # Common mistakes in tesseract
        if text=='3)':
            text='5'        
        if text == '4)':
            text='6'
        if text == ')':
            text='9'
        
        number = re.sub(r'\D', '', text)
        if debug == '1':
            padded_image.save(f'Point{count}.png')
            pyautogui.moveTo(x,y)
            print('Is this a ',number)
            ask=input()
            if(ask=='r'): #in debugging, this will remove a value if its wrong, ie: getting a 10 and then re reading the 1 or 0 
                number=''
            pyautogui.moveTo(10,10)

        if number.isdigit():
            final_list.append((int(number),(x,y)))
        count+=1

    final_list.sort()
    #print(final_list)
    for point in final_list:
        word,point=point
        print(word)
        #pyautogui.moveTo(point,duration=0.125)
        pyautogui.click(point)
    
def chimp_test(num):
    for i in range(num):     
        pyautogui.click(continue_location)       #continue
        pyautogui.moveTo(10,10)         #move mouse off screen so numbers are clear       
        run_stage()                     #click every number

# Change 20 to whatever score you want
chimp_test(20)
