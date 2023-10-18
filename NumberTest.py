import pytesseract
import pyautogui
import time

# Path to the Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Use PrintCoords.py to get coordinates of the white bar under the numbers being displayed
# click at close as possible to the left edge in the white area
timer_location = 790, 614
start_location=852,715 #start button and submit button
number_box_location = (200, 426, 1500, 175) # x, y, width, height

def wait_for_pixel_color_change():
    color = pyautogui.pixel(timer_location)
    while True:
        # Get the current pixel color at (x, y) in the specified region
        current_color = pyautogui.pixel(timer_location)
        if color !=current_color:
            break  # Exit the loop if the color has changed
        # Pause briefly before checking the pixel again (adjust the duration as needed)
        pyautogui.sleep(0.1)

count=0
# Function to extract text from a specified region of the screen
def extract_text_from_screenshot(region):
    global count
    count+=1
    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=region).convert("L")
    #screenshot.save(f'TypingTest{count}.png')

    # Use Tesseract to do OCR on the screenshot
    text = pytesseract.image_to_string(screenshot,config='--psm 6 -l eng')
    numbers = ''.join(filter(str.isdigit, text))
    
    return numbers


def get_and_type_number():
    
    text = extract_text_from_screenshot(number_box_location)

    wait_for_pixel_color_change()

    time.sleep(1)
    #print('typing',text)
    pyautogui.click(805, 542)
    pyautogui.write(text)
    pyautogui.click(845, 664) #submit
    time.sleep(2)
    pyautogui.click(841, 742) #next

#click to start game
pyautogui.click(start_location)

for i in range(20):
    get_and_type_number()
    

    


