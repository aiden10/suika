import time
import pyautogui
import random

cherryRGB = (114, 176, 107)
strawberryRGB = (224, 112, 74)
grapeRGB = (225, 117, 247)
dekoponRGB = (255, 167, 60)
orangeRGB = (228, 139, 84)
backgroundRGB = (255, 225, 174)
def capture_screen_segment(x, y, width, height):
    screenshot = pyautogui.screenshot()
    segment = screenshot.crop((x, y, x + width, y + height))
    return segment

def top_fruits(game_board):
    width, height = game_board.size
    cherry = []
    c_found = False
    strawberry = []
    s_found = False
    grape = []
    g_found = False
    dekopon = []
    d_found = False
    orange = []
    o_found = False
    for y in range(height):
        for x in range(width):
            # if y > 20:
            #     if not c_found: # be looking for a cherry
            #         if game_board.getpixel((x, y)) == cherryRGB and game_board.getpixel((x, y - 20)) == backgroundRGB:
            #             cherry.append([x + 700, y + 280])
            #             c_found = True
            #             print('cherry found')
            #
            #     if not s_found: # be looking for a strawberry
            #         if game_board.getpixel((x, y)) == strawberryRGB and game_board.getpixel((x, y - 20)) == backgroundRGB:
            #             strawberry.append([x + 700, y + 280])
            #             s_found = True
            #             print('strawberry found')
            #
            #     if not g_found: # be looking for a grape
            #         if game_board.getpixel((x, y)) == grapeRGB and game_board.getpixel((x, y - 20)) == backgroundRGB:
            #             grape.append([x + 700, y + 280])
            #             g_found = True
            #             print('grape found')
            #
            #     if not d_found: # be looking for a dekopon
            #         if game_board.getpixel((x, y)) == dekoponRGB and game_board.getpixel((x, y - 20)) == backgroundRGB:
            #             dekopon.append([x + 700, y + 280])
            #             d_found = True
            #             print('dekopon found')
            #
            #     if not o_found: # be looking for a orange
            #         if game_board.getpixel((x, y)) == orangeRGB and game_board.getpixel((x, y - 20)) == backgroundRGB:
            #             orange.append([x + 700, y + 280])
            #             o_found = True
            #             print('orange found')
            if not c_found:  # be looking for a cherry
                if game_board.getpixel((x, y)) == cherryRGB:
                    cherry.append([x + 700, y + 280])
                    c_found = True
                    print('cherry found')

            if not s_found:  # be looking for a strawberry
                if game_board.getpixel((x, y)) == strawberryRGB:
                    strawberry.append([x + 700, y + 280])
                    s_found = True
                    print('strawberry found')

            if not g_found:  # be looking for a grape
                if game_board.getpixel((x, y)) == grapeRGB:
                    grape.append([x + 700, y + 280])
                    g_found = True
                    print('grape found')

            if not d_found:  # be looking for a dekopon
                if game_board.getpixel((x, y)) == dekoponRGB:
                    dekopon.append([x + 700, y + 280])
                    d_found = True
                    print('dekopon found')

            if not o_found:  # be looking for a orange
                if game_board.getpixel([x, y]) == orangeRGB:
                    orange.append([x + 700, y + 280])
                    o_found = True
                    print('orange found')

    return cherry, strawberry, grape, dekopon, orange

while True:
    randomLeft = random.randint(-200, -50)
    randomRight = random.randint(50, 150)

    screen = capture_screen_segment(700, 280, 600, 1000)
    game_board = screen.crop((15, 0, 505, 700))

    current_fruit = capture_screen_segment((1920 / 2) - 50, 150, 100, 100)

    cherryPos, strawberryPos, grapePos, dekoponPos, orangePos = top_fruits(game_board)

    if current_fruit.getpixel((50, 70)) == cherryRGB:
        print("cherry")
        if cherryPos:
            pyautogui.click(cherryPos[0][0], 800)
        else:
            pyautogui.click((1920/2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == strawberryRGB:
        print("strawberry")
        if strawberryPos:
            pyautogui.click(strawberryPos[0][0], 800)
        else:
            pyautogui.click((1920/2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == grapeRGB:
        print("grape")
        if grapePos:
            pyautogui.click(grapePos[0][0], 800)
        else:
            pyautogui.click((1920/2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == dekoponRGB:
        print("dekopon")
        if dekoponPos:
            pyautogui.click(dekoponPos[0][0], 800)
        else:
            pyautogui.click((1920/2) + randomLeft, 800)

    if current_fruit.getpixel((50, 70)) == orangeRGB:
        print("orange")
        if orangePos:
            pyautogui.click(orangePos[0][0], 800)
        else:
            pyautogui.click((1920/2) + randomRight, 800)

    time.sleep(1)


# determines which side to place fruits
# while True:
#     current_fruit = capture_screen_segment((1920 / 2) - 50, 150, 100, 100)
#     randomLeft = random.randint(-200, -50)
#     randomRight = random.randint(50, 150)
#
#     if (current_fruit.getpixel((50, 70)) == cherryRGB):
#         pyautogui.click((1920/2) + randomRight, 800)
#         print("cherry")
#
#     if (current_fruit.getpixel((50, 70)) == strawberryRGB):
#         pyautogui.click((1920/2) + randomRight, 800)
#         print("strawberry")
#     if (current_fruit.getpixel((50, 70)) == grapeRGB):
#         pyautogui.click((1920/2) + randomRight, 800)
#         print("grape")
#     if (current_fruit.getpixel((50, 70)) == dekoponRGB):
#         pyautogui.click((1920/2) + randomLeft, 800)
#         print("dekopon")
#     if (current_fruit.getpixel((50, 70)) == orangeRGB):
#         pyautogui.click((1920/2) + randomLeft, 800)
#         print("orange")
#
#     time.sleep(1)


# focus left, and double click
#
# randomX = random.randint(-240, 240)
# if 240 > randomX > 0:
#     randomX = random.randint(-240, 240)
# pyautogui.click((1920/2) + randomX, 800)
# time.sleep(1)
# pyautogui.click((1920/2) + randomX, 800)
# time.sleep(1)

# double click

# randomX = random.randint(-240, 240)
# pyautogui.click((1920/2) + randomX, 800)
# time.sleep(1)
# pyautogui.click((1920/2) + randomX, 800)
# time.sleep(1)

# focus left
# randomX = random.randint(-240, 240)
# if 240 > randomX > 0:
#     randomX = random.randint(-240, 240)
# pyautogui.click((1920/2) + randomX, 800)
# time.sleep(1)
