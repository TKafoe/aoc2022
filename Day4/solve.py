def fully_contains(int1, int2):
	return int1[0] <= int2[0] and int1[1] >= int2[1]

def overlaps(int1, int2):
	return int1[0] <= int2[1] and int2[0] <= int1[1]

num = 0
with open('input.txt', 'r') as f:
	data = f.read().splitlines()
	for row in data:
		intervals = row.split(',')
		int1 = (int(intervals[0].split('-')[0]), int(intervals[0].split('-')[1]))
		int2 = (int(intervals[1].split('-')[0]), int(intervals[1].split('-')[1]))
		if overlaps(int1, int2):
			num += 1

	print(num)