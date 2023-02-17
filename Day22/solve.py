import re
import math

WIDTH = 50

ORIENTATION_MAPPING = {
	("<", "<"): 0,
	("<", "^"): 90,
	("<", ">"): 180,
	("<", "v"): -90,

	("^", "<"): -90,
	("^", "^"): 0,
	("^", ">"): 90,
	("^", "v"): 180,

	(">", "<"): 180,
	(">", "^"): -90,
	(">", ">"): 0,
	(">", "v"): 90,

	("v", "<"): 90,
	("v", "^"): 180,
	("v", ">"): -90,
	("v", "v"): 0,
}

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return int(qx) % WIDTH, int(qy) % WIDTH


def correct_orientation(pos, prev_or, new_or, mirror):
	val = 0
	if prev_or == "v" or prev_or == "^":
		val = pos[0] if not mirror else WIDTH - pos[0] - 1
	if prev_or == "<" or prev_or == ">":
		val = pos[1] if not mirror else WIDTH - pos[1] - 1

	if new_or == "v":
		new_pos = val, 0
	if new_or == "^":
		new_pos = val, WIDTH - 1
	if new_or == "<":
		new_pos = WIDTH - 1, val
	if new_or == ">":
		new_pos = 0, val
	return new_pos

class DiceSide:
	def __init__(self, side, yoffset, xoffset):
		self.b = None
		self.b_or = None
		self.b_mirrored = None
		self.t = None
		self.t_or = None
		self.t_mirrored = None
		self.r = None
		self.r_or = None
		self.r_mirrored = None
		self.l = None
		self.l_or = None
		self.l_mirrored = None
		self.side = side
		self.xoffset = xoffset
		self.yoffset = yoffset

	def set_top(self, top, orientation, mirror):
		self.t = top
		self.t_or = orientation
		self.t_mirrored = mirror

	def set_bottom(self, bottom, orientation, mirror):
		self.b = bottom
		self.b_or = orientation
		self.b_mirrored = mirror

	def set_right(self, right, orientation, mirror):
		self.r = right
		self.r_or = orientation
		self.r_mirrored = mirror

	def set_left(self, left, orientation, mirror):
		self.l = left
		self.l_or = orientation
		self.l_mirrored = mirror

	def move(self, pos, delta, orientation):
		n_pos = (pos[0] + delta[0], pos[1] + delta[1])
	
		if n_pos[0] >= WIDTH:
			n_pos = (pos[0] - delta[0], pos[1] - delta[1])
			n_pos = correct_orientation(n_pos, orientation, self.r_or, self.r_mirrored)
			return self.r.side[n_pos[1]][n_pos[0]], self.r, n_pos, self.r_or
		if n_pos[0] < 0:
			n_pos = (pos[0] - delta[0], pos[1] - delta[1])
			n_pos = correct_orientation(n_pos, orientation, self.l_or, self.l_mirrored)
			return self.l.side[n_pos[1]][n_pos[0]], self.l, n_pos, self.l_or
		if n_pos[1] >= WIDTH:
			n_pos = (pos[0] - delta[0], pos[1] - delta[1])
			n_pos = correct_orientation(n_pos, orientation, self.b_or, self.b_mirrored)
			return self.b.side[n_pos[1]][n_pos[0]], self.b, n_pos, self.b_or
		if n_pos[1] < 0:
			n_pos = (pos[0] - delta[0], pos[1] - delta[1])
			n_pos = correct_orientation(n_pos, orientation, self.t_or, self.t_mirrored)
			return self.t.side[n_pos[1]][n_pos[0]], self.t, n_pos, self.t_or

		return self.side[n_pos[1]][n_pos[0]], self, n_pos, orientation

FACING = {
	3: "^",
	0: ">",
	1: "v",
	2: "<"
}

FACING_REV = {
	"^": 3,
	">": 0,
	"v": 1,
	"<": 2
}

DELTAS = {
	3: (0, -1),
	0: (1, 0),
	1: (0, 1),
	2: (-1, 0)
}


def process_path_with_dice(path, dice):
	pos = (0, 0)
	facing = 0
	cur_side = dice[0][1]
	i = 0
	for step in path:
		# if i == 100:
			# break
		steps = int(step[:len(step) - 1])
		d = DELTAS[facing]

		for _ in range(steps):
			b, n_side, n_pos, orientation = cur_side.move(pos, d, FACING[facing])
			if b == "#":
				break
			facing = FACING_REV[orientation]
			d = DELTAS[facing]
			pos = n_pos
			cur_side = n_side
			n_side.side[n_pos[1]][n_pos[0]] = FACING[facing]

		if step[-1] == "X":
			pass
		elif step[-1] == "R":
			facing += 1
		else:
			facing -= 1
		facing %= 4

		i += 1

	return pos, facing, cur_side


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

	i = 0
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

def build_cube(grid):
	dice = []
	for i in range(4):
		row = []
		for j in range(3):
			row.append(DiceSide([grid[l][j*WIDTH:(j+1)*WIDTH] for l in range(i * WIDTH, (i+1) * WIDTH)], i, j))
		dice.append(row)

	# dice[0][2].set_top(dice[1][0], "v", True)
	# dice[1][0].set_top(dice[0][2], "v", True)

	# dice[0][2].set_left(dice[1][1], "v", False)
	# dice[1][1].set_top(dice[0][2], ">", False)

	# dice[0][2].set_right(dice[2][3], "<", True)
	# dice[0][3].set_right(dice[0][2], "<", True)

	# dice[0][2].set_bottom(dice[1][2], "v", False)
	# dice[1][2].set_top(dice[0][2], "^", False)

	# dice[1][0].set_left(dice[2][3], "^", True)
	# dice[2][3].set_bottom(dice[1][0], ">", True)

	# dice[1][0].set_right(dice[1][1], ">", False)
	# dice[1][1].set_left(dice[1][0], "<", False)

	# dice[1][0].set_bottom(dice[2][2], "^", True)
	# dice[2][2].set_bottom(dice[1][0], "^", True)

	# dice[1][1].set_bottom(dice[2][2], ">", True)
	# dice[2][2].set_left(dice[1][1], "^", True)

	# dice[1][1].set_right(dice[1][2], ">", False)
	# dice[1][2].set_left(dice[1][1], "<", False)

	# dice[1][2].set_right(dice[2][3], "v", True)
	# dice[2][3].set_top(dice[1][2], "<", True)

	# dice[1][2].set_bottom(dice[2][2], "v", False)
	# dice[2][2].set_top(dice[1][2], "^", False)

	# dice[2][2].set_right(dice[2][3], ">", False)
	# dice[2][3].set_left(dice[2][2], "<", False)


	dice[0][1].set_top(dice[3][0], ">", False)
	dice[3][0].set_left(dice[0][1], "v", False)

	dice[0][1].set_left(dice[2][0], ">", True)
	dice[2][0].set_left(dice[0][1], ">", True)

	dice[0][1].set_right(dice[0][2], ">", False)
	dice[0][2].set_left(dice[0][1], "<", False)

	dice[0][1].set_bottom(dice[1][1], "v", False)
	dice[1][1].set_top(dice[0][1], "^", False)

	dice[0][2].set_top(dice[3][0], "^", False) # not sure
	dice[3][0].set_bottom(dice[0][2], "v", False)

	dice[0][2].set_bottom(dice[1][1], "<", False)
	dice[1][1].set_right(dice[0][2], "^", False)

	dice[0][2].set_right(dice[2][1], "<", True)
	dice[2][1].set_right(dice[0][2], "<", True)

	dice[1][1].set_left(dice[2][0], "v", False)
	dice[2][0].set_top(dice[1][1], ">", False)

	dice[1][1].set_bottom(dice[2][1], "v", False)
	dice[2][1].set_top(dice[1][1], "^", False)

	dice[2][0].set_right(dice[2][1], ">", False)
	dice[2][1].set_left(dice[2][0], "<", False)

	dice[2][0].set_bottom(dice[3][0], "v", False)
	dice[3][0].set_top(dice[2][0], "^", False)

	dice[2][1].set_bottom(dice[3][0], "<", False)
	dice[3][0].set_right(dice[2][1], "^", False)

	return dice

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

		# pos, facing = process_path(path, grid)

		dice = build_cube(grid)
		pos, facing, cur_side = process_path_with_dice(path, dice)

		print(pos[1] + (cur_side.yoffset*WIDTH) + 1)
		print(1000 * (pos[1] + (cur_side.yoffset*WIDTH) + 1) + 4 * (pos[0] + (cur_side.xoffset*WIDTH) + 1) + facing)
		print(facing)

		s = ""
		for i in range(len(dice)):
			for k in range(WIDTH):
				for j in range(len(dice[i])):
					s += "".join(dice[i][j].side[k])
				s += "\n"

		print(s)

if __name__ == "__main__":
	main()