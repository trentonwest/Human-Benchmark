import pytesseract
from PIL import Image
import pyautogui

# Path to the Tesseract executable (you need to install Tesseract on your system)
# You only need this if tesseract isnt in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Store the words in a list
word_list = []

# What score to stop at
limit=200

# Use PrintCoords.py to find the coordinates, for word_region (x, y, width, height)
# and a single pixel location for where the start, seen, and new buttons are
word_region = (323, 484, 1200, 150)
seen_location=777, 660
new_location=930, 660
start_location = 855,746



# Function to click at specific coordinates
def click_at(x, y):
    pyautogui.click(x, y)

# Function to extract words from the screenshot using OCR
def extract_words_from_screenshot():
    screenshot = pyautogui.screenshot(region=word_region)
    #screenshot.save('screenshot.png')
    extracted_text = pytesseract.image_to_string(screenshot)
    word=extracted_text.strip().split()
    return word



pyautogui.click(start_location)
count=0
while True:
    # Get words from the screenshot
    word = extract_words_from_screenshot()
    
    if word in word_list:
        pyautogui.click(seen_location)
    else:
        word_list.append(word)
        pyautogui.click(new_location)
    #print(f'Processed word: {word}')
    
    count+=1
    if count>limit:
        break

