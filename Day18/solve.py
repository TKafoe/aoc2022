class Cube:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.sides = 6

	def connect(self, cube):
		self.sides -= 1
		cube.sides -= 1

def create_cube(x, y, z, grid, cubes, mx, my, mz):
	cube = Cube(x, y, z)
	cubes.append(cube)
	grid[x][y][z] = cube

	if x - 1 <= mx and x - 1 >= 0 and grid[x - 1][y][z] != None:
		grid[x - 1][y][z].connect(cube)
	if x + 1 <= mx and x + 1 >= 0 and grid[x + 1][y][z] != None:
		grid[x + 1][y][z].connect(cube)
	if y - 1 <= my and y - 1 >= 0 and grid[x][y - 1][z] != None:
		grid[x][y - 1][z].connect(cube)
	if y + 1 <= my and y + 1 >= 0 and grid[x][y + 1][z] != None:
		grid[x][y + 1][z].connect(cube)
	if z - 1 <= mz and z - 1 >= 0 and grid[x][y][z - 1] != None:
		grid[x][y][z - 1].connect(cube)
	if z + 1 <= mz and z + 1 >= 0 and grid[x][y][z + 1] != None:
		grid[x][y][z + 1].connect(cube)

def dfs(p, grid, visited, mx, my, mz):
	visited.add(p)
	x = p[0]
	y = p[1]
	z = p[2]

	if x <= 0 or x >= mx:
		return True
	if y <= 0 or y >= my:
		return True
	if z <= 0 or z >= mz:
		return True

	if x - 1 <= mx and x - 1 >= 0 and grid[x - 1][y][z] == None and (x - 1, y, z) not in visited:
		if dfs((x - 1, y, z), grid, visited, mx, my, mz):
			return True
	if x + 1 <= mx and x + 1 >= 0 and grid[x + 1][y][z] == None and (x + 1, y, z) not in visited:
		if dfs((x + 1, y, z), grid, visited, mx, my, mz):
			return True
	if y - 1 <= my and y - 1 >= 0 and grid[x][y - 1][z] == None and (x, y - 1, z) not in visited:
		if dfs((x, y - 1, z), grid, visited, mx, my, mz):
			return True
	if y + 1 <= my and y + 1 >= 0 and grid[x][y + 1][z] == None and (x, y + 1, z) not in visited:
		if dfs((x, y + 1, z), grid, visited, mx, my, mz):
			return True
	if z - 1 <= mz and z - 1 >= 0 and grid[x][y][z - 1] == None and (x, y, z - 1) not in visited:
		if dfs((x, y, z - 1), grid, visited, mx, my, mz):
			return True
	if z + 1 <= mz and z + 1 >= 0 and grid[x][y][z + 1] == None and (x, y, z + 1) not in visited:
		if dfs((x, y, z + 1), grid, visited, mx, my, mz):
			return True

	return False


def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()

		mx = max([int(row.split(",")[0]) for row in data])
		my = max([int(row.split(",")[1]) for row in data])
		mz = max([int(row.split(",")[2]) for row in data])

		print(mx)
		print(my)
		print(mz)

		grid = [[[None for _ in range(mz + 1)] for _ in range(my + 1)] for _ in range(mx + 1)]
		cubes = []
		for row in data:
			x, y, z = [int(a) for a in row.split(",")]
			create_cube(x, y, z, grid, cubes, mx, my, mz)

		print(sum([cube.sides for cube in cubes]))
		changed = True
		while changed:
			changed = False
			for i in range(mx + 1):
				for j in range(my + 1):
					for k in range(mz + 1):
						if grid[i][j][k] == None and not dfs((i, j, k), grid, set(), mx, my, mz):
							create_cube(i, j, k, grid, cubes, mx, my, mz)
							changed = True
		print(sum([cube.sides for cube in cubes]))

if __name__ == "__main__":
	main()
