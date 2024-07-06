"""
Can try using the data about the fruits' positions to decide a different way of placing fruits.
Like summing the values in the left and right and trying to keep them balanced. 
"""
import numpy as np
import cv2
import math
import pyautogui
import random
from mss import mss
from bisect import bisect_left
from PIL import Image

class Fruit:
    def __init__(self, x, y, radius, value):
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)
        self.connections = set()
        self.value = value
    def __str__(self):
        return list(FRUIT_VALUES_TABLE.keys())[list(FRUIT_VALUES_TABLE.values()).index(self.value)]
    def __repr__(self):
        return self.__str__()
    
# might modify this to have a list for r, g, and b values for each fruit
COLOR_KEYS = [500, 540, 565, 580, 590, 610, 625, 640, 650, 675, 700, 710] 
highest_fruit = 'cherry'
score = -1
chain = ()

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

FRUIT_VALUES_TABLE = {
    'cherry': 1,
    'strawberry': 2,
    'grape': 3,
    'dekopon': 4,
    'orange': 5,
    'apple': 6,
    'pear': 7,
    'peach': 8,
    'pineapple': 9,
    'melon': 10,
    'watermelon': 11
}
bounding_box = {'top': 175, 'left': 715, 'width': 490, 'height': 800}
sct = mss()

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

def is_intersecting(fruit1, fruit2):
    x1, y1, r1 = fruit1.x, fruit1.y, fruit1.radius
    x2, y2, r2 = fruit2.x, fruit2.y, fruit2.radius
    
    # Calculate the distance between the centers of the fruits
    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx * dx + dy * dy)
    
    # Define a small overlap threshold (you may need to adjust this value)
    overlap_threshold = 10  
    
    # Check if the fruits are touching or slightly overlapping
    return distance <= (r1 + r2 + overlap_threshold)

def get_intersections(fruits):
    fruit_objects = {}
    for f in fruits:
        circle_data, name = f
        value = FRUIT_VALUES_TABLE[name]
        fruit = Fruit(circle_data[2][0], circle_data[2][1], circle_data[1], value)
        fruit_objects[name] = fruit
    
    for fruit in fruit_objects.values():
        for other_fruit in fruit_objects.values():
            if fruit != other_fruit and is_intersecting(fruit, other_fruit):
                fruit.connections.add(other_fruit)
                other_fruit.connections.add(fruit)

    return list(fruit_objects.values())

def get_chain_recursive(fruit, first_fruit, held_fruit, chain=None, visited=None, depth=0):
    """
    I don't think this should be using the held fruit every time 
    But it also does need to still use it somehow
    """
    if chain is None:
        chain = ()
    if visited is None:
        visited = []

    # Base case: if we've looped back to the first fruit and it's not the start
    if fruit == first_fruit and depth > 0 or fruit in visited:
        return {chain: 0}
    
    current_chain = chain + (fruit,)
    visited.append(fruit)
    best_chain = {current_chain: 0}

    for adjacent_fruit in fruit.connections:
        value_difference = adjacent_fruit.value - held_fruit.value
        if 0 <= value_difference <= 3:
            sub_chains = get_chain_recursive(adjacent_fruit, first_fruit, held_fruit, current_chain, visited, depth + 1)
            for sub_chain, sub_score in sub_chains.items():
                score = sub_score
                if value_difference == 1:
                    score += 4
                elif value_difference == 0:
                    score += 3
                elif value_difference == 2:
                    score += 2
                elif value_difference == 3:
                    score += 1
                
                if score > best_chain.get(sub_chain, 0):
                    best_chain[sub_chain] = score
    
    visited = None
    
    return best_chain

def get_chain(fruit, current_fruit):
    chains = get_chain_recursive(fruit, fruit, current_fruit)
    return max(chains.items(), key=lambda x: x[1])

def is_fruit_covered(fruit, fruits):
    x_threshold = 50
    for other_fruit in fruits:
        if abs(fruit.x - other_fruit.x) < x_threshold and other_fruit.y > fruit.y:
            return True

    return False

def place_fruit(fruits, current_fruit):
    current_fruit_object = Fruit(0, 0, 0, FRUIT_VALUES_TABLE[current_fruit])
    chains = {}
    for fruit in fruits:
        chain = get_chain(fruit, current_fruit_object)
        chains.update({fruit: chain})

    chains = dict(sorted(chains.items(), key=lambda item: item[1][1], reverse=True))
    for chain in chains:
        if not is_fruit_covered(fruit, fruits):
            best = next(iter(chains.items()))
            fruit_chain = best[1][0]
            score = best[1][1]
            pyautogui.click(chain.x + 715, chain.y + 175)
            return fruit_chain, score
    
    pyautogui.click(715 + random.randint(0, 300), 500) # for if there are no detected fruits 
    return (), -1

def draw_connections(frame, fruits):
    for fruit in fruits:
        for connected_fruit in fruit.connections:
            cv2.line(frame, 
                     (int(fruit.x), int(fruit.y)), 
                     (int(connected_fruit.x), int(connected_fruit.y)), 
                     (100, 100, 100), 1)  

def draw_chain(frame, chain, score):
    for i in range(len(chain) - 1):
        fruit1 = chain[i]
        fruit2 = chain[i + 1]
        cv2.line(frame, 
                (int(fruit1.x), int(fruit1.y)), 
                (int(fruit2.x), int(fruit2.y)), 
                (255, 255, 0), 2)  

    cv2.putText(frame, f'Chain Score: {score}', (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
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
    # elif radius > 155:
    #     return 'watermelon'
    else:
        return 'unknown'

def identify_circles(frame, wait):
    global highest_fruit, score, chain
    fruits = []
    frame = np.asarray(frame)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, 1.2, 40, param1=110,param2=50,minRadius=10,maxRadius=180)
    ys = {}
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            cv2.circle(mask, (circle[0], circle[1]), circle[2], (255, 255, 255), -1)
            avg_rgb = cv2.mean(frame, mask=mask)[::-1]
            circle_data = (int((avg_rgb[0] + avg_rgb[1] + avg_rgb[2])), circle[2], (circle[0], circle[1]))
            fruit = identify_fruit(circle_data) 
            if fruit != 'unknown':
                fruits.append((circle_data, fruit))
                ys.update({fruit : circle[1]})
                cv2.putText(frame, fruit, (circle[0], circle[1]), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2) # draw the outer circle
                cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3) # draw the center of the circle

        fruits = sorted(fruits, key=lambda x: x[1])
        connections = get_intersections(fruits)
        draw_connections(frame, connections)
        ys_sorted = dict(sorted(ys.items(), key=lambda item: item[1]))

        if len(ys_sorted) > 0:
            first = next(iter(ys_sorted))
            if ys_sorted[first] < 80:
                highest_fruit = first

        cv2.putText(frame, f'Dropping: {highest_fruit}', (185, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if wait == 0:
            chain, score = place_fruit(connections, highest_fruit)

        if score != -1 and len(chain) > 0:
            draw_chain(frame, chain, score)

    return frame

def main():
    wait = 0
    while True:
        if wait == 30: wait = 0
        sct_img = sct.grab(bounding_box)
        frame = identify_circles(sct_img, wait)
        cv2.imshow('screen', np.array(frame))
        cv2.setWindowProperty('screen', cv2.WND_PROP_TOPMOST, 1)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        wait += 1
        
main()