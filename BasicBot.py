# Bot which attempts to 'intelligently' determine where to place fruit
import time
import pyautogui
import random

cherryTopRGB = (141, 164, 118)
cherryRGB = (225, 79, 137)
strawberryRGB = (223, 112, 78)
strawberryWhite = (253, 199, 198)
strawberryLeaf = (195, 219, 164)
grapeRGB = (225, 117, 247)
dekoponRGB = (255, 167, 60)
orangeRGB = (228, 139, 84)
orangeLeaf = (29, 192, 56)
backgroundRGB = (255, 225, 174)
endColor = (25, 22, 17)
click_count = 0
SCORE_MULT = 7.325

def capture_screen_segment(x, y, width, height):
    screenshot = pyautogui.screenshot()
    segment = screenshot.crop((x, y, x + width, y + height))
    return segment

def top_fruits(game_board):
    width, height = game_board.size
    cherry, strawberry, grape, dekopon, orange = [], [], [], [], []
    c_found, s_found, g_found, d_found, o_found = False, False, False, False, False
    game_over = False

    for y in range(height):
        for x in range(width):
            if game_board.getpixel((x, y)) == endColor:
                game_over = True
                print(f"Game Over detected at ({x}, {y})")
                return cherry, strawberry, grape, dekopon, orange, game_over

            if y > 40:
                if not c_found and game_board.getpixel((x, y)) == cherryRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                    cherry.append([x + 700, y + 280])
                    c_found = True
                    print('Topmost cherry found at', x, y)

                if not s_found and (game_board.getpixel((x, y)) in {strawberryLeaf, strawberryRGB} or (game_board.getpixel((x, y - 50)) == strawberryWhite and game_board.getpixel((x, y - 50)) == backgroundRGB)):
                    strawberry.append([x + 700, y + 280])
                    s_found = True
                    print('Topmost strawberry found at', x, y)

                if not g_found and game_board.getpixel((x, y)) == grapeRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                    grape.append([x + 700, y + 280])
                    g_found = True
                    print('Topmost grape found at', x, y)

                if not d_found and game_board.getpixel((x, y)) == dekoponRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                    dekopon.append([x + 700, y + 280])
                    d_found = True
                    print('Topmost dekopon found at', x, y)

                if not o_found and game_board.getpixel((x, y)) == orangeLeaf and game_board.getpixel((x, y - 40)) == backgroundRGB:
                    orange.append([x + 700, y + 280])
                    o_found = True
                    print('Topmost orange found at', x, y)
            else:
                if not c_found and game_board.getpixel((x, y)) == cherryRGB:
                    cherry.append([x + 700, y + 280])
                    c_found = True
                    print('Cherry found at', x, y)

                if not s_found and game_board.getpixel((x, y)) in {strawberryLeaf, strawberryRGB, strawberryWhite}:
                    strawberry.append([x + 700, y + 280])
                    s_found = True
                    print('Strawberry found at', x, y)

                if not g_found and game_board.getpixel((x, y)) == grapeRGB:
                    grape.append([x + 700, y + 280])
                    g_found = True
                    print('Grape found at', x, y)

                if not d_found and game_board.getpixel((x, y)) == dekoponRGB:
                    dekopon.append([x + 700, y + 280])
                    d_found = True
                    print('Dekopon found at', x, y)

                if not o_found and game_board.getpixel((x, y)) == orangeLeaf:
                    orange.append([x + 700, y + 280])
                    o_found = True
                    print('Orange found at', x, y)
    return cherry, strawberry, grape, dekopon, orange, game_over

while True:
    click_count += 1
    randomLeft = random.randint(-200, -50)
    randomRight = random.randint(50, 150)

    screen = capture_screen_segment(700, 280, 600, 1000)
    game_board = screen.crop((15, 0, 505, 700))
    current_fruit = capture_screen_segment(int((1920 / 2) - 50), 150, 100, 100)
    cherryPos, strawberryPos, grapePos, dekoponPos, orangePos, game_over = top_fruits(game_board)

    fruit_pixel = current_fruit.getpixel((50, 70))
    print(f"Current fruit RGB: {fruit_pixel}")

    if fruit_pixel == cherryTopRGB:
        print("Current fruit: Cherry")
        if cherryPos:
            pyautogui.click(cherryPos[0][0] + 10, cherryPos[0][1])
        else:
            pyautogui.click(int(1920 / 2) + randomRight, 800)

    elif fruit_pixel == strawberryRGB:
        print("Current fruit: Strawberry")
        if strawberryPos:
            pyautogui.click(strawberryPos[0][0], strawberryPos[0][1])
        elif cherryPos:
            pyautogui.click(cherryPos[0][0] + 10, cherryPos[0][1])
        else:
            pyautogui.click(int(1920 / 2) + randomRight, 800)

    elif fruit_pixel == grapeRGB:
        print("Current fruit: Grape")
        if grapePos:
            pyautogui.click(grapePos[0][0], grapePos[0][1])
        elif strawberryPos:
            pyautogui.click(strawberryPos[0][0], strawberryPos[0][1])
        else:
            pyautogui.click(int(1920 / 2) + randomRight, 800)

    elif fruit_pixel == dekoponRGB:
        print("Current fruit: Dekopon")
        if dekoponPos:
            pyautogui.click(dekoponPos[0][0], dekoponPos[0][1])
        elif orangePos:
            pyautogui.click(orangePos[0][0], orangePos[0][1])
        else:
            pyautogui.click(int(1920 / 2) + randomLeft, 800)

    elif fruit_pixel == orangeRGB:
        print("Current fruit: Orange")
        if orangePos:
            pyautogui.click(orangePos[0][0] + 10, orangePos[0][1])
        else:
            pyautogui.click(int(1920 / 2) + randomLeft, 800)

    if game_over:
        print("Game over")
        with open("scoresA.txt", "a") as f:
            f.write(f"Score: {click_count * SCORE_MULT}\n")

        pyautogui.click(int(1920 / 2), 800)
        click_count = 0

    if click_count > 550:
        pyautogui.click(115, 84)
        click_count = 0

    time.sleep(1)
