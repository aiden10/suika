# Suika Game Bot
## Basic Algorithm Bot
![ezgif com-video-to-gif](https://github.com/aiden10/suika/assets/51337166/00ab5085-a71d-455e-b6bc-52cdfe563dd9)
### Strategy
Looks at held fruit and looks for the highest matching fruit. If it exists, the bot places it on top of the matching fruit. If it does not exist, fruits one tier up are searched for and the current fruit gets placed on it. Otherwise, fruits are placed semi-randomly. Cherries, strawberries, and grapes are placed randomly on the right side and dekopons and oranges are placed randomly on the left side. 
### Stats
- Average score: 1366
- Lowest score: 842
- Highest score: 2212
  
<sup>*These values were calculated from 72 games and scores are approximate</sup>

## Gemini Pro Vision Bot
![Recording2024-06-06174256-Trim-ezgif com-video-to-gif-converter(1)(1)(1)](https://github.com/aiden10/suika/assets/51337166/ef995226-72fb-4358-9272-cc7097f7f94a)

### Strategy
The Gemini Vision API is given a screenshot of the game with a 10x10 grid drawn over it along with this prompt:

```
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
```
Pyautogui is then used to navigate the cursor to the desired cell and click. Also a different prompt and different tips may result in a performance change.

**Example Screenshot**

![screenshot](https://github.com/aiden10/suika/assets/51337166/ab520f82-3de0-4cff-95fa-b63d71ec2759)

### Stats
- Average score: 1026
- Lowest score: 922
- Highest score: 1142
  
<sup>*These values were calculated from 9 games and scores are approximate</sup>

