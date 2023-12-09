import time
import pyautogui
import random

cherryTopRGB = (114, 176, 107)
cherryRGB = (225, 79, 137)
strawberryRGB = (224, 112, 74)
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
    game_over = False
    for y in range(height):
        for x in range(width):
            if y > 40:
                if not c_found:  # be looking for a cherry
                    if game_board.getpixel((x, y)) == cherryRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                        cherry.append([x + 700, y + 280])
                        c_found = True
                        print('topmost cherry found')

                if not s_found:  # be looking for a strawberry
                    if game_board.getpixel((x, y)) == strawberryLeaf or game_board.getpixel(
                            (x, y)) == strawberryRGB or game_board.getpixel(
                            (x, y - 50)) == strawberryWhite and game_board.getpixel((x, y - 50)) == backgroundRGB:
                        strawberry.append([x + 700, y + 280])
                        s_found = True
                        print('topmost strawberry found')

                if not g_found:  # be looking for a grape
                    if game_board.getpixel((x, y)) == grapeRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                        grape.append([x + 700, y + 280])
                        g_found = True
                        print('topmost grape found')

                if not d_found:  # be looking for a dekopon
                    if game_board.getpixel((x, y)) == dekoponRGB and game_board.getpixel((x, y - 40)) == backgroundRGB:
                        dekopon.append([x + 700, y + 280])
                        d_found = True
                        print('topmost dekopon found')

                if not o_found:  # be looking for an orange
                    if game_board.getpixel((x, y)) == orangeLeaf and game_board.getpixel((x, y - 40)) == backgroundRGB:
                        orange.append([x + 700, y + 280])
                        o_found = True
                        print('topmost orange found')
            else:
                if not c_found:  # be looking for a cherry
                    if game_board.getpixel((x, y)) == cherryRGB:
                        cherry.append([x + 700, y + 280])
                        c_found = True
                        print('cherry found')

                if not s_found:  # be looking for a strawberry
                    if game_board.getpixel((x, y)) == strawberryLeaf or game_board.getpixel(
                            (x, y)) == strawberryRGB or game_board.getpixel((x, y)) == strawberryWhite:
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

                if not o_found:  # be looking for an orange
                    if game_board.getpixel([x, y]) == orangeLeaf:
                        orange.append([x + 700, y + 280])
                        o_found = True
                        print('orange found')
                if game_board.getpixel([x, y]) == endColor:
                    game_over = True
    return cherry, strawberry, grape, dekopon, orange, game_over


while True:
    click_count += 1
    randomLeft = random.randint(-200, -50)
    randomRight = random.randint(50, 150)

    screen = capture_screen_segment(700, 280, 600, 1000)
    game_board = screen.crop((15, 0, 505, 700))

    current_fruit = capture_screen_segment((1920 / 2) - 50, 150, 100, 100)

    cherryPos, strawberryPos, grapePos, dekoponPos, orangePos, game_over = top_fruits(game_board)

    if current_fruit.getpixel((50, 70)) == cherryTopRGB:
        print("cherry")
        if cherryPos:
            pyautogui.click(cherryPos[0][0] + 10, cherryPos[0][1])
        else:
            pyautogui.click((1920 / 2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == strawberryRGB:
        print("strawberry")
        if strawberryPos:
            pyautogui.click(strawberryPos[0][0], strawberryPos[0][1])
        elif cherryPos:
            pyautogui.click(cherryPos[0][0] + 10, cherryPos[0][1])
        else:
            pyautogui.click((1920 / 2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == grapeRGB:
        print("grape")
        if grapePos:
            pyautogui.click(grapePos[0][0], grapePos[0][1])
        elif strawberryPos:
            pyautogui.click(strawberryPos[0][0], strawberryPos[0][1])
        else:
            pyautogui.click((1920 / 2) + randomRight, 800)

    if current_fruit.getpixel((50, 70)) == dekoponRGB:
        print("dekopon")
        if dekoponPos:
            pyautogui.click(dekoponPos[0][0], dekoponPos[0][1])
        elif orangePos:
            pyautogui.click(orangePos[0][0], orangePos[0][1])
        else:
            pyautogui.click((1920 / 2) + randomLeft, 800)

    if current_fruit.getpixel((50, 70)) == orangeRGB:
        print("orange")
        if orangePos:
            pyautogui.click(orangePos[0][0] + 10, orangePos[0][1])
        else:
            pyautogui.click((1920 / 2) + randomLeft, 800)

    if game_over:
        f = open("scores.txt", "a")
        print("game over")
        f.write(f"Score: {click_count * SCORE_MULT}\n")
        f.close()

        pyautogui.click((1920 / 2), 800)
        click_count = 0

    if click_count > 550:
        pyautogui.click(115, 84)
        click_count = 0

    time.sleep(1)
