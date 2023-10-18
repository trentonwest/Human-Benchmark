import pytesseract
from PIL import ImageDraw
import pyautogui
import time

# Path to the Tesseract executable (you need to install Tesseract on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

area = 607, 344, 1096, 834              #coords of area
feild = 607, 344, 1096-607, 834-344     #x,y,width,height
level_area= 621, 254, 809-621, 305-254  #cheks what level were on
start_location = 852, 715

def generate_grid(num_points):
    x_min, y_min, x_max, y_max = area
    step_x = (x_max - x_min) / num_points
    step_y = (y_max - y_min) / num_points

    center_points = []
    for i in range(num_points):
        for j in range(num_points):
            x = int(x_min + i * step_x + step_x / 2)
            y = int(y_min + j * step_y + step_y / 2)
            center_points.append((x, y))

    return center_points

def get_static_color(point,screenshot):
    x,y=point
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color

def get_pixel_color(point):
    x, y = point
    return pyautogui.pixel(x, y)

def get_white_list(points):
    #print('getting whites')
    sequence=[]
    screenshot = pyautogui.screenshot()
    #cropped=screenshot.crop(area)
    #draw = ImageDraw.Draw(cropped)
    
    for point in points:
        #cropped_xy= point[0]-area[0],point[1]-area[1]
        color = get_static_color(point,screenshot)
        if color[0]>=200:   #just check if the red value is high cuz the screens normally blue
            sequence.append(point)
            #draw.rectangle([cropped_xy,cropped_xy], outline="black", width=4)

    #cropped.save('VisMem.png')
    return sequence

def wait_til_clear(point):                      
    while True:
        #print('waiting to clear board before clicking')
        color = get_pixel_color(point)
        if color != (255,255,255):
            time.sleep(0.25)
            return

def click_em(points):
    #print('clickin')
    for point in points:
        pyautogui.click(point)

def next_round():
    screenshot = pyautogui.screenshot(region=level_area)  # Define the region coordinates (x, y, width, height) accordingly
    #screenshot.save('level.png')
    extracted_text = pytesseract.image_to_string(screenshot)
    word=extracted_text.strip().split()
    while True:
        #print('waiting')
        screenshot = pyautogui.screenshot(region=level_area)
        #screenshot.save('nex_level.png')
        extracted_text = pytesseract.image_to_string(screenshot)
        word2=extracted_text.strip().split()
        if word != word2:
            time.sleep(0.35)
            #print('GO!')
            return
        
def start():
    global level
    points = generate_grid(3)
    level+=1
    #imediatly look for white pixels
    click_this = get_white_list(points)
    #wait till boards clear
    wait_til_clear(click_this[0])
    #click them all
    click_em(click_this)
    
    level+=1

    #wait till next round starts
    next_round()

    #get new pixels
    click_this = get_white_list(points)
    #wait till boards clear
    wait_til_clear(click_this[0])
    #click them all
    click_em(click_this)

    play()

def play():
    global level
    round_structure = [(3,4),(3,5),(5,6),(5,7),(5,8),(10,9)]

    for round in round_structure:
        rounds, grid_size = round  
        points = generate_grid(grid_size)
        for i in range(rounds):
            level+=1
            #wait till next round starts
            next_round()

            #get new pixels
            start=time.time()
            click_this = get_white_list(points)
            #wait till boards clear
            wait_til_clear(click_this[0])
            time_end=time.time()
            print(f'{level} Time for level computation {(time_end-start):.2f}\n')
            #click them all
            click_em(click_this)     

#start game
pyautogui.click(start_location)
time.sleep(.75)
level=0

start()
