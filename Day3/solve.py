import string

with open('input.txt', 'r') as f:
	data = f.read().splitlines()

	s = 0
	for i in range(0, len(data), 3):
		common = set(data[i]).intersection(data[i+1]).intersection(data[i+2]).pop()
		s += list(string.ascii_letters).index(common) + 1

	print(s)