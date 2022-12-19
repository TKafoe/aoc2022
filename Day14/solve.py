def draw_line(grid, start, end):
	if start[0] == end[0]:
		if start[1] > end[1]:
			for i in range(end[1], start[1] + 1):
				grid[start[0]][i] = "#"
		else:
			for i in range(start[1], end[1] + 1):
				grid[start[0]][i] = "#"
	else:
		if start[0] > end[0]:
			for i in range(end[0], start[0] + 1):
				grid[i][start[1]] = "#"
		else:
			for i in range(start[0], end[0] + 1):
				grid[i][start[1]] = "#"

def store_lines(data):
	leftmin = 1000
	rightmax = 0
	bottommax = 0
	grid = [["." for _ in range(6000)] for _ in range(200)]
	for row in data:
		lines = row.split(" -> ")
		for i in range(len(lines) - 1):
			p1x, p1y = [int(x) for x in lines[i].split(",")]
			p2x, p2y = [int(x) for x in lines[i+1].split(",")]

			if p1x < leftmin:
				leftmin = p1x
			if p1x > rightmax:
				rightmax = p1x
			if p2x < leftmin:
				leftmin = p2x
			if p2x > rightmax:
				rightmax = p2x
			if p1y > bottommax:
				bottommax = p1y
			if p2y > bottommax:
				bottommax = p2y

			draw_line(grid, (p1y, p1x), (p2y, p2x))

	return grid, leftmin, rightmax, bottommax

def print_grid(grid, l, r, b):
	for i, row in enumerate(grid):
		if i < (b + 2):
			printable = row[l-80:r+1+80]
			print("".join(printable))

def sand_step(grid, pos, b):
	if pos[0] + 1 == b + 2:
		grid[pos[0]][pos[1]] = "o"
		return (0, 500), False
	if grid[pos[0] + 1][pos[1]] == ".":
		pos = (pos[0] + 1, pos[1])
		return pos, False
	if grid[pos[0] + 1][pos[1] - 1] == ".":
		pos = (pos[0] + 1, pos[1] - 1)
		return pos, False
	if grid[pos[0] + 1][pos[1] + 1] == ".":
		pos = (pos[0] + 1, pos[1] + 1)
		return pos, False

	grid[pos[0]][pos[1]] = "o"
	if pos == (0, 500):
		return (0, 500), True
	return (0, 500), False

def flow_sand(grid, b):
	pos = (0, 500)
	s = 0
	found = False
	while not found:
		pos, found = sand_step(grid, pos, b)
		if pos == (0, 500):
			s += 1

	return s

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		grid, l, r, b = store_lines(data)
		s = flow_sand(grid, b)
		print_grid(grid, l, r, b)
		print(s)


if __name__ == "__main__":
	main()