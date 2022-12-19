import numpy as np

def handle_H(H, direction):
	if direction == "U":
		return (H[0], H[1] + 1)
	if direction == "D":
		return (H[0], H[1] - 1)
	if direction == "L":
		return (H[0] - 1, H[1])
	if direction == "R":
		return (H[0] + 1, H[1])

def handle_T(T, H):
	if np.sqrt((H[0] - T[0])**2 + (H[1] - T[1])**2) <= np.sqrt(2):
		return T

	dx = (H[0] - T[0]) / (abs(H[0] - T[0])) if H[0] != T[0] else 0
	dy = (H[1] - T[1]) / (abs(H[1] - T[1])) if H[1] != T[1] else 0
	return (T[0] + dx, T[1] + dy)
	
with open('input.txt', 'r') as f:
	data = f.read().splitlines()
	
	T = [(0,0) for _ in range(9)]
	visited = set()
	visited.add((0,0))
	H = (0,0)
	for row in data:
		direction, num = row.split(" ")

		for i in range(int(num)):
			H = handle_H(H, direction)
			T[0] = handle_T(T[0], H)
			for j in range(1, len(T)):
				T[j] = handle_T(T[j], T[j - 1])
				if j == 8:		
					visited.add(T[j])

	print(len(visited))

