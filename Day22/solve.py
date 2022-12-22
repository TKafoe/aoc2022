import re

FACING = {
	3: "^",
	0: ">",
	1: "v",
	2: "<"
}

DELTAS = {
	3: (0, -1),
	0: (1, 0),
	1: (0, 1),
	2: (-1, 0)
}


def get_left_most_i(row, grid):
	return next(i for i, val in enumerate(grid[row]) if val != " ")
def get_right_most_i(row, grid):
	return len(grid[row]) - 1 - next(i for i, val in enumerate(grid[row][::-1]) if val != " ")
def get_top_most_i(col, grid):
	return next(i for i in range(len(grid)) if grid[i][col] != " ")
def get_bottom_most_i(col, grid):
	return next(i for i in range(len(grid) - 1, -1, -1) if grid[i][col] != " ")

def process_path(path, grid):
	pos = (get_left_most_i(0, grid), 0)
	facing = 0

	for step in path:
		steps = int(step[:len(step) - 1])
		d = DELTAS[facing]

		for _ in range(steps):
			new_pos = (pos[0] + d[0] , pos[1] + d[1])

			if FACING[facing] == "<" and new_pos[0] < get_left_most_i(new_pos[1], grid):
				new_pos = (get_right_most_i(new_pos[1], grid), new_pos[1])
			if FACING[facing] == ">" and new_pos[0] > get_right_most_i(new_pos[1], grid):
				new_pos = (get_left_most_i(new_pos[1], grid), new_pos[1])
			if FACING[facing] == "v" and new_pos[1] > get_bottom_most_i(new_pos[0], grid):
				new_pos = (new_pos[0], get_top_most_i(new_pos[0], grid))
			if FACING[facing] == "^" and new_pos[1] < get_top_most_i(new_pos[0], grid):
				new_pos = (new_pos[0], get_bottom_most_i(new_pos[0], grid))

			if grid[new_pos[1]][new_pos[0]] == "#":
				break

			pos = new_pos
			grid[new_pos[1]][new_pos[0]] = FACING[facing]

		if step[-1] == "X":
			pass
		elif step[-1] == "R":
			facing += 1
		else:
			facing -= 1
		facing %= 4

	return pos, facing

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		path = re.findall(r"(\d+[A-Z])", data[-1])
		path.append("10X")
		grid = [list(x) for x in data[0:-2]]
		mxl = max([len(r) for r in grid])
		for row in grid:
			while len(row) < mxl:
				row.append(" ")

		print(path)
		pos, facing = process_path(path, grid)
		print(1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing)

		# for r in grid:
			# print("".join(r))

if __name__ == "__main__":
	main()