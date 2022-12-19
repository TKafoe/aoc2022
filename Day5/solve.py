import re

def move_one(stack, start, end):
	moved = stack[start - 1].pop()
	stack[end - 1].append(moved)

def move(stack, num, start, end):
	for _ in range(num):
		move_one(stack, start, end)
	stack[end - 1][len(stack[end - 1]) - num:] = stack[end - 1][-num:][::-1]

stack = [[] for i in range(9)]
with open('input.txt', 'r') as f:
	data = f.read().splitlines()

	for j in range(8):
		row = data[j]
		for i in range(9):
			if row[i*4 + 1] != " ":
				stack[i] = [row[i*4 + 1]] + stack[i]

	for row in data[10:]:
		numbers = list(map(int, re.findall(r'\d+', row)))
		move(stack, numbers[0], numbers[1], numbers[2])

	st = ""
	for s in stack:
		st += str(s.pop())
	print(st)
