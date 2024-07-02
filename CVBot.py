"""
using opencv
use HoughCircles function to get list of detected circles
get the average rgb of each circle, do that a few times to determine the average rgb of each fruit, and sum them to get a unique value for each fruit
also store the average radius of each fruit
compare each cirlces summed average rgb (look at nearest value) to the known fruit values to determine what each fruit is 

go over each fruit's position (hopefully x,y is middle of circle) and see if it overlaps with any other fruit
assign each fruit on the board a unique key
Example:
detection_threshold = 5 # pixels
touching_fruits = {}
for fruit in fruits:
    current_fruit_x, current_fruit_y, current_fruit_radius, current_fruit_key = fruit[0], fruit[1], fruit[2], fruit[3]
    for other_fruit in fruits:
        other_fruit_x, other_fruit_y, other_fruit_radius, other_fruit_key = other_fruit[0], other_fruit[1], other_fruit[2], other_fruit[3]
        
        touching = (abs(current_fruit_radius - other_fruit_radius) <= 
        (math.sqrt((current_fruit_x - other_fruit_x)^2 + (current_fruit_y - other_fruit_y)^2)) <= 
        ((current_fruit_radius + other_fruit_radius + detection_threshold)))

        if touching:
            exists = graph.find(current_fruit_key) # imaginary graph class and function which goes over each node and finds it
            if exists:
                touching_fruits.add(fruit) # use a set so there are no duplicates
                touching_fruits.add(other_fruit)
                graph.add(fruit, other_fruit) # finds the first argument and connects it to the second argument

I'm guessing that a graph could be implemented the same way that binary trees are except instead of a single pointer to
its next node, it'd have a list of pointers to its next nodes
the graph also needs to be directed to be able to find the longest path but if they're touching then they would be pointing to eachother
search the graph to find the best fruit chain. 
ideal fruit chain would be increasing rank by one each node
so each node/fruit should also have its rank 
cherry -> strawberry -> grape -> dekopon, etc
Traversing:
paths = {}
for fruit in touching_fruits:
    length = graph.find_longest_path(fruit) # this function would need to prioritize the connections where rank increases by one 
    path = {fruit: length}

longest_chain = max(paths.items()) 
fruit, length = longest_chain.items()[0]

fruit_x, fruit_y = fruit[0], fruit[1]
pyautogui.click(fruit_x, fruit_y)
although I would also need to check if the space above the fruit is clear or not before dropping it... 

after the graph has been created and the fruits are there it'd be cool to see a visualization        
"""
import numpy as np
import cv2
from mss import mss
from bisect import bisect_left
from PIL import Image

# might modify this to have a list for r, g, and b values for each fruit
COLOR_KEYS = [500, 540, 565, 580, 590, 610, 625, 640, 650, 675, 700, 710] 
FRUIT_TABLE = {
    500: 'unknown',
    540: 'cherry',
    550: 'unknown',
    580: 'strawberry',
    565: 'grape',
    675: 'dekopon',
    610: 'orange',
    590: 'apple',
    700: 'pear',
    625: 'peach',
    710: 'pineapple',
    640: 'unknown',
    650: 'melon'
}
def take_closest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before
    
def identify_fruit(circle_data):
    color_sum = circle_data[0]
    radius = circle_data[1]
    fruit_color = take_closest(COLOR_KEYS, color_sum)

    # some fruits have distinct enough sizes so I don't need to bother identifying them by color
    if radius > 15 and radius < 20:
        return 'cherry'
    elif radius > 22 and radius < 30 and (fruit_color == 580 or fruit_color == 565):
        return 'strawberry'
    elif radius > 36 and radius < 43 and fruit_color == 675:
        return 'dekopon'
    elif radius > 30 and radius < 44 and (fruit_color == 565 or fruit_color == 580):
        return 'grape'
    elif radius > 45 and radius < 54 and fruit_color == 610:
        return 'orange'
    elif radius > 55 and radius < 64 and (fruit_color == 590 or fruit_color == 580):
        return 'apple'
    elif radius > 55 and radius < 64 and (fruit_color == 700 or fruit_color == 675):
        return 'pear'
    elif radius > 80 and radius < 90 and (fruit_color == 625 or fruit_color == 610):
        return 'peach'
    elif radius > 97 and radius < 110 and fruit_color == 710:
        return 'pineapple'
    elif radius > 130 and radius < 155 and fruit_color == 650:
        return 'melon'
    else:
        return 'unknown'
    
def identify_circles(frame):
    
    fruits = []
    frame = np.asarray(frame)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, 1.2, 40, param1=110,param2=50,minRadius=10,maxRadius=180)
    ys = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            cv2.circle(mask, (circle[0], circle[1]), circle[2], (255, 255, 255), -1)
            avg_rgb = cv2.mean(frame, mask=mask)[::-1]
            circle_data = (int((avg_rgb[0] + avg_rgb[1] + avg_rgb[2])), circle[2], (circle[0], circle[1]))
            fruit = identify_fruit(circle_data) 
            # fruits.append((round(avg_rgb[0], 2), round(avg_rgb[1], 2), round(avg_rgb[2], 2)))
            if fruit != 'unknown':
                fruits.append((circle_data, fruit))
                ys.append({fruit : circle[1]})
                cv2.putText(frame, fruit, (circle[0], circle[1]), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2) # draw the outer circle
                cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3) # draw the center of the circle
        fruits = sorted(fruits, key=lambda x: x[1])
        print(fruits)
        ys_sorted = sorted(ys, key=lambda d: list(d.values())[0])
        if len(ys_sorted) > 0:
            highest_fruit = next(iter(ys_sorted[0].keys()))
            cv2.putText(frame, f'Dropping: {highest_fruit}', (185, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    return frame

bounding_box = {'top': 175, 'left': 715, 'width': 490, 'height': 800}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)
    frame = identify_circles(sct_img)
    cv2.imshow('screen', np.array(frame))
    cv2.setWindowProperty('screen', cv2.WND_PROP_TOPMOST, 1)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break