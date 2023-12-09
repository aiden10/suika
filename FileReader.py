lines = []
scores = []
total = 0
average = 0

with open('scores.txt') as file:
    for line in file:
        lines.append(line.strip().split(':')[1:])
file.close()

del lines[0]

for score in lines:
    score = float(score[0])
    total += score
    scores.append(score)
average = total / len(lines)
print(average)
print(min(scores))
print(max(scores))