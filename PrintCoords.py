from pynput import mouse

# Counter for the number of clicks
click_count = 0
coordList=[]
# Function to handle mouse click event
def on_click(x, y, button, pressed):
    global click_count
    if pressed:
        click_count += 1
        coordList.append((x,y))
        if click_count >= 2:
            print(coordList)
            return False

# Set up the listener to call the on_click function on mouse click events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
