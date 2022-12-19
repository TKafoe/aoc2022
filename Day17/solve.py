import math

ROCKS = [
	[
		[True, True, True, True]
	],
	[
		[False, True, False],
		[True, True, True],
		[False, True, False],
	],
	[
		[False, False, True],
		[False, False, True],
		[True, True, True],
	],
	[
		[True],
		[True],
		[True],
		[True],
	],
	[
		[True, True],
		[True, True],
	]
]

class Board:
	def __init__(self):
		self.board = [[False for _ in range(7)]]

	def add_rock(self, p, rock_i):
		for _ in range(p[1] - len(self.board) + 1):
			self.board.append([False for _ in range(7)])

		rock = ROCKS[rock_i]
		for i, row in enumerate(rock):
			for j, val in enumerate(row):
				if val:
					self.board[p[1] - i][p[0] + j] = val

	def can_move(self, p, rock_i):
		for _ in range(p[1] - len(self.board) + 1):
			self.board.append([False for _ in range(7)])

		rock = ROCKS[rock_i]
		if p[0] + len(rock[0]) - 1 > 6 or p[0] < 0:
			return False
		if p[1] - len(rock) + 1 < 0:
			return False
		for i, row in enumerate(rock):
			for j, val in enumerate(row):
				if val and self.board[p[1] - i][p[0] + j]:
					return False
		return True

	def get_max_height(self):
		return max([i if any(row) else 0 for i, row in enumerate(self.board)])

	def __str__(self):
		s = ""

		for row in self.board:
			s += "".join(["#" if val else "." for val in row]) + "\n"

		return s

def step(p, rock, action, floor):
	if action == ">" and floor.can_move((p[0] + 1, p[1]), rock):
		p = (p[0] + 1, p[1])
	if action == "<" and floor.can_move((p[0] - 1, p[1]), rock):
		p = (p[0] - 1, p[1])

	if not floor.can_move((p[0], p[1] - 1), rock):
		floor.add_rock(p, rock)
		return True, p
	else:
		p = (p[0], p[1] - 1)
		return False, p

def main():
	with open('input.txt', 'r') as f:
		data = f.read()

		floor = Board()
		rock = 0
		p = (2, 3)
		action_num = 0

		D = {}
		base = 0
		cycle = 0
		base_height = 0
		cycle_height = 0
		cycle_found = False
		done = False

		actions = []
		while rock <= 1000000000000:
			action = data[action_num]
			stopped, p = step(p, rock % 5, action, floor)
			if stopped:
				heights.append(floor.get_max_height() + 1)

				rock += 1
				if rock % 5 == 1 or rock % 5 == 2:
					p = (2, floor.get_max_height() + 6)
				elif rock % 5 == 3:
					p = (2, floor.get_max_height() + 7)
				elif rock % 5 == 4:
					p = (2, floor.get_max_height() + 5)
				else:
					p = (2, floor.get_max_height() + 4)

				if not cycle_found:
					if (action_num, rock % 5, str(floor.board[-12:])) not in D:
						D[(action_num, rock % 5, str(floor.board[-12:]))] = (rock, floor.get_max_height() + 1)
					else:
						cycle = rock - D[(action_num, rock % 5, str(floor.board[-12:]))][0]
						base = D[(action_num, rock % 5, str(floor.board[-12:]))][0] - 1
						base_height = D[(action_num, rock % 5, str(floor.board[-12:]))][1]
						cycle_height = floor.get_max_height() + 1 - base_height
						cycle_found = True

						num = (1000000000000 - rock) // cycle
						rem = (1000000000000 - rock) % cycle
						height_added = cycle_height * num
						rock += num * cycle

			action_num += 1
			action_num %= len(data)

		print(floor.get_max_height() + height_added)

if __name__ == "__main__":
	main()