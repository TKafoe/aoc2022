import numpy as np

def is_visible(r, c, data):
	if r == 0 or r == data.shape[0] - 1 or c == 0 or c == data.shape[1]:
		return True

	return not (
		any(x >= data[r][c] for x in data[r][0:c])
		and any(x >= data[r][c] for x in data[r][c + 1:])
		and any(x >= data[r][c] for x in data[:,c][0:r])
		and any(x >= data[r][c] for x in data[:,c][r + 1:]))

def scenic_score(r, c, data):
	sc = 1
	sc *= next((i + 1 for i, x in enumerate(data[r][0:c][::-1]) if x >= data[r][c]), c)
	sc *= next((i + 1 for i, x in enumerate(data[r][c + 1:]) if x >= data[r][c]), len(data[r][c + 1:]))
	sc *= next((i + 1 for i, x in enumerate(data[:,c][0:r][::-1]) if x >= data[r][c]), r)
	sc *= next((i + 1 for i, x in enumerate(data[:,c][r + 1:]) if x >= data[r][c]), len(data[:,c][r + 1:]))
	return sc

with open('input.txt', 'r') as f:
	data = np.array([list(l) for l in f.read().splitlines()])
	print(sum([1 if is_visible(x, y, data) else 0 for x in range(data.shape[0]) for y in range(data.shape[1])]))
	print(max([scenic_score(x, y, data) for x in range(data.shape[0]) for y in range(data.shape[1])]))
