import pyautogui
import os
import shutil
import json
import time
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
import cv2

SCORE_MULT = 7.325
END_COLOR = (25, 21, 3)
click_count = 0
CURRENT_DIR = os.getcwd()
screenshots_folder = os.path.join(CURRENT_DIR, 'screenshots')
PATH = os.path.join(screenshots_folder, 'screenshot.png')
load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')
safety_config = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },

    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },

]

def parse_response(response):
    response = response.replace('`', "").strip()
    response = response.replace('json', "")
    data = json.loads(response)
    data = json.loads(response)
    X = data["X"]
    Y = data["Y"]
    thoughts = data["Thoughts"]
    return float(X), float(Y), str(thoughts)

def perform_actions(x, y):
    global click_count
    click_count += 1
    pyautogui.moveTo((x * 48) + 720, (y * 10) + 280)    
    pyautogui.click()
    time.sleep(1)

def restart():
    global click_count
    print('Game Over')
    with open("scores.txt", "a") as f:
        f.write(f"Score: {click_count * SCORE_MULT}\n")

    click_count = 0
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)

def delete_screenshots():
    for filename in os.listdir(screenshots_folder):
        file_path = os.path.join(screenshots_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def screenshot(left, upper, right, lower):
    screenshot = pyautogui.screenshot(PATH)
    segment = screenshot.crop((left, upper, right, lower))
    width, height = segment.size
    screen_image = np.array(segment) # screenshot
    screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
    grid_image = np.zeros_like(screen_image) # grid image file

    num_rows = 10
    num_cols = 10
    row_height = height // num_rows
    col_width = width // num_cols

    # Draw horizontal lines (21 high)
    for i in range(num_rows + 1):
        y = i * row_height
        cv2.line(grid_image, (0, y), (width, y), (255, 255, 255), 1)

    # Draw vertical lines (38 wide)
    for j in range(num_cols + 1):
        x = j * col_width 
        
        cv2.line(grid_image, (x, 0), (x, height), (255, 255, 255), 1)

    final_image = cv2.addWeighted(screen_image, 1, grid_image, 0.5, 0) # put grid on top off screenshot
    cv2.imwrite(PATH, final_image)

def main():
    delete_screenshots()
    screenshot(left=710, upper=185, right=1200, lower=960)

    if not os.path.isfile(PATH):
        raise SystemExit("No screenshot found")
    image = Image.open(PATH)
    if image.getpixel((50, 20)) == END_COLOR:
        restart()

    prompt = f"""
                Based on what you see in the screenshot, I would like you to play Suika Game to the best of your abilities. Suika Game, in case you
                don't already know, is a game similar to 2048 but instead is played by dropping fruits which then combine to form larger fruits.
                You will see a fruit at the top of the screen, when you click, the fruit will be dropped. 
                On top of the screenshot, I have overlayed a 10 x 10 grid. To interact with the game and drop fruit, please write the X,Y position
                of the cell where you would like to drop the current fruit.
                Here are some tips:
                    - Consider the momentum
                    - Use fruits to knock another fruit
                    - Never throw a tiny fruit between two larger fruits
                    - Just because you can merge two fruits does not always mean you should

                Expected response format: 
                    {{
                    "X": x cell coordinate (0 - 10),
                    "Y": y cell coordinate (0 - 10),
                    "Thoughts": "I think that..."
                    }}
                    You must always leave the X and Y fields filled with a number from 0 to 10.
                    If you have no thoughts then write "" in the "Thoughts" field.
                """ 

    print('generating response...')
    response = model.generate_content([prompt, image], safety_settings=safety_config)

    # after a response is recieved
    x, y, thoughts = parse_response(response.text)
    perform_actions(x, y)
    print()
    print(thoughts)
    print()
    delete_screenshots()
    return

while True:
    main()
