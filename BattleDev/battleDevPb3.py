
"""
Deux versions la première en prenant une carte zones et en plaçant les points cultivables
autour des X 
la seconde en se plaçant sur un point et en cherchant les zones cultivables autour de celui-ci
"""

lines = []

with open('./pb3/input1.txt', 'r') as inputs:
    for line in inputs:
    	lines.append(line.rstrip()) # retire le \n de fin de ligne


N = int(lines[0])
# on retire la première valeur qui est un renseignement sur la taille de la grille
lines = lines[1:]

# l'idée est de remplir les zones vide de zone cultivable
zones = [[0 for _ in range(N)] for _ in range(N)]

for y, line in enumerate(lines):
	for x, point in enumerate(line):
		if point == 'X':
			if y > 0 and lines[y-1][x] != 'X':
				zones[y-1][x] = 1

			if y < N - 1 and lines[y+1][x] != 'X':
				zones[y+1][x] = 1

			if x > 0 and lines[y][x-1] != 'X':
				zones[y][x-1] = 1

			if x < N - 1 and lines[y][x+1] != 'X':
				zones[y][x+1] = 1
			
			if x > 0 and y > 0 and lines[y-1][x-1] != 'X':
				zones[y-1][x-1] = 1

			if x < N - 1 and y > 0 and lines[y-1][x+1] != 'X':
				zones[y-1][x+1] = 1
			
			if y < N - 1 and x > 0 and lines[y+1][x-1] != 'X':
				zones[y+1][x-1] = 1

			if y < N- 1 and x < N - 1 and lines[y+1][x+1] != 'X':
				zones[y+1][x+1] = 1


# à la fin on compte les zones cultivables
count = 0
for line in zones:
	count += line.count(1)

print(count)

# second version

count = 0

for y, line in enumerate(lines):
	for x, point in enumerate(line):
		if point == '.':
			if y > 0 and lines[y-1][x] == 'X':
				count += 1
				continue

			if y < N - 1 and lines[y+1][x] == 'X':
				count += 1
				continue

			if x > 0 and lines[y][x-1] == 'X':
				count += 1
				continue

			if x < N - 1 and lines[y][x+1] == 'X':
				count += 1
				continue
			
			if x > 0 and y > 0 and lines[y-1][x-1] == 'X':
				count += 1
				continue

			if x < N - 1 and y > 0 and lines[y-1][x+1] == 'X':
				count += 1
				continue
			
			if y < N - 1 and x > 0 and lines[y+1][x-1] == 'X':
				count += 1
				continue

			if y < N- 1 and x < N - 1 and lines[y+1][x+1] == 'X':
				count += 1
				continue

print(count)
