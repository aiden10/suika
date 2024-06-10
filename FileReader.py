lines = []
scores = []
total = 0
average = 0

with open('scoresC.txt') as file:
    for line in file:
        lines.append(line.strip().split(':')[1:])
file.close()

del lines[0]

for score in lines:
    score = float(score[0])
    total += score
    scores.append(score)
average = total / len(lines)
print(f'Games Played: {len(scores) + 1}')
print(f'Average: {average}')
print(f'Lowest: {min(scores)}')
print(f'Highest: {max(scores)}')
