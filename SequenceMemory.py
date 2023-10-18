import pyautogui
import time

# Define the locations to check on the screen
# Use PrintCoords.py, change the value in there to get 9 locations and copy past the reult here
locations = [(679, 423),(851, 426),(1019, 415),(682, 583),(855, 577),(1019, 587),(680, 753),(851, 746),(1003, 759)]
start_location=852,715
# Score to get
limit=30

def is_white(color):
    return color[0] > 200 and color[1] > 200 and color[2] > 200

def find_boxes():
    changed_locations = []
    last_change_time = time.time()
    while True:
        # Flag to check if any box changed color during this iteration
        box_changed = False
        for location in locations:
            color = pyautogui.pixel(location[0], location[1])

            if is_white(color):
                changed_locations.append(location)
                box_changed = True
                last_change_time = time.time()

                #wait for it to not be white, then continue
                while is_white(pyautogui.pixel(location[0], location[1])):
                    pass

        # If no box changed color for 1.5 seconds, stop the monitoring
        if not box_changed and time.time() - last_change_time >= 1.5:
            break
    return(changed_locations)

def click_points_in_order(points,score):
    if score>limit:
        exit(0)
    score+=1
    for point in points:
        #pyautogui.moveTo(point,duration=0.5)
        pyautogui.click(point)
    click_points_in_order(find_boxes(),score)

#start the game
pyautogui.click(start_location)
click_points_in_order(find_boxes(),0)