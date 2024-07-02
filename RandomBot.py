# Bot which randomly places fruit (control)
# Play area X range: 720 - 1200

import pyautogui
import time
import random
import os
import shutil
from PIL import Image

CURRENT_DIR = os.getcwd()
screenshots_folder = os.path.join(CURRENT_DIR, 'screenshots')
PATH = os.path.join(screenshots_folder, 'screenshot.png')
END_COLOR = (25, 21, 3)
SCORE_MULT = 7.325
click_count = 0

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
    segment.save(PATH)

def restart():
    global click_count
    print('Game Over')
    with open("scoresC.txt", "a") as f:
        f.write(f"Score: {(click_count * SCORE_MULT) - 30}\n")

    click_count = 0
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)

while True:
    delete_screenshots()
    screenshot(left=710, upper=185, right=1200, lower=960)

    if not os.path.isfile(PATH):
        raise SystemExit("No screenshot found")
    image = Image.open(PATH)
    if image.getpixel((50, 20)) == END_COLOR:
        restart()

    time.sleep(1)
    randomX = random.randint(720, 1200)
    pyautogui.click((randomX, 400)) # Y value doesn't really matter
    click_count += 1
    print(click_count)
    if click_count > 400:
        pyautogui.hotkey('ctrl', 'r')
        click_count = 0