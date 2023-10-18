import pytesseract
import pyautogui

# Path to the Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the coordinates of the region to capture (left, top, width, height), and any place inside the typing area
region_coordinates = (215, 526, 1500, 300)
input_box=294,574

translation_table = str.maketrans({'|':'I','\n': ' ',  '\t': ' ', '\r': None})

# Function to extract text from a specified region of the screen
def extract_text_from_screenshot(region):
    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=region)
    #screenshot.save('TypingTest.png')

    # Use Tesseract to do OCR on the screenshot
    text = pytesseract.image_to_string(screenshot)
    return text.translate(translation_table)

def type_it(text):
    # click input feild
    pyautogui.click(input_box)
    pyautogui.write(text)


# Extract text from the specified region
extracted_text = extract_text_from_screenshot(region_coordinates)

# Print the extracted text 
print("Extracted text from the specified region:")
print(extracted_text)

type_it(extracted_text)

    


