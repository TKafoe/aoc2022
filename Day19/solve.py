import re
import numpy as np


# def step(m, storage, rates, queue, bps):
# 	if m >= 24:
# 		return storage[3]
# 	# Update rates
# 	rates += queue

# 	# Pick options

# 	# storage[0] // bps[0] == x
# 	# storage[0] // bps[1] == y
# 	# min(storage[0] // bps[2], storage[1] // bps[3]) == z
# 	# min(storage[0] // bps[4], storage[2] // bps[5]) == a
# 	# x * bps[0] + y * bps[1] + z * bps[2] + a * bps[4] <= storage[0]
# 	# z * bps[3] <= storage[1]
# 	# a * bps[5] <= storage[2]
# 	# x >= 0
# 	# y >= 0
# 	# z >= 0
# 	# a >= 0
# 	# options = [np.array([0, 0, 0, 0])]
# 	# if storage[0] // bps[0] > 0:
# 	# 	options.append(np.array([1, 0, 0, 0]))
# 	# if storage[0] // bps[1] > 0:
# 	# 	options.append(np.array([0, 1, 0, 0]))
# 	# if min(storage[0] // bps[2], storage[1] // bps[3]) > 0:
# 	# 	options = [np.array([0, 0, 1, 0])]
# 	# if min(storage[0] // bps[4], storage[2] // bps[5]) > 0:
# 	# 	options = [np.array([0, 0, 0, 1])]

# 	storage += rates

# 	mx = 0
# 	temp_storage = storage.copy()
# 	temp_m = m
# 	option = np.array([1, 0, 0, 0])
# 	while rates[0] > 0 and temp_storage[0] // bps[0] == 0:
# 		temp_storage += rates
# 		temp_m += 1
	
# 	if temp_storage[0] // bps[0] > 0:
# 		cost = np.array([
# 			bps[0] * option[0] + bps[1] * option[1] + bps[2] * option[2] + bps[4] * option[3],
# 			bps[3] * option[2],
# 			bps[5] * option[3],
# 			0
# 			])
# 		temp_val = step(temp_m + 1, temp_storage - cost, rates.copy(), option, bps) > m
# 		if temp_val > mx:
# 			mx = temp_val
	
# 	option = np.array([0, 1, 0, 0])
# 	temp_storage = storage.copy()
# 	temp_m = m
# 	while rates[0] > 0 and rates[2] > 0 and temp_storage[0] // bps[1] == 0:
# 		temp_storage += rates
# 		temp_m += 1

# 	if temp_storage[0] // bps[1] > 0:
# 		cost = np.array([
# 			bps[0] * option[0] + bps[1] * option[1] + bps[2] * option[2] + bps[4] * option[3],
# 			bps[3] * option[2],
# 			bps[5] * option[3],
# 			0
# 			])
# 		temp_val = step(temp_m + 1, temp_storage - cost, rates.copy(), option, bps) > m
# 		if temp_val > mx:
# 			mx = temp_val

# 	np.array([0, 0, 1, 0])
# 	temp_storage = storage.copy()
# 	temp_m = m
# 	while rates[0] > 0 and rates[2] > 0 and min(temp_storage[0] // bps[2], temp_storage[1] // bps[3]) == 0:
# 		temp_storage += rates
# 		temp_m += 1

# 	if min(temp_storage[0] // bps[2], temp_storage[1] // bps[3]) > 0:
# 		cost = np.array([
# 			bps[0] * option[0] + bps[1] * option[1] + bps[2] * option[2] + bps[4] * option[3],
# 			bps[3] * option[2],
# 			bps[5] * option[3],
# 			0
# 			])
# 		temp_val = step(temp_m + 1, temp_storage - cost, rates.copy(), option, bps) > m
# 		if temp_val > mx:
# 			mx = temp_val
	
# 	np.array([0, 0, 0, 1])
# 	temp_storage = storage.copy()
# 	temp_m = m
# 	while rates[0] > 0 and rates[2] > 0 and min(temp_storage[0] // bps[4], temp_storage[2] // bps[5]) == 0:
# 		temp_storage += rates
# 		temp_m += 1
# 		cost = np.array([
# 			bps[0] * option[0] + bps[1] * option[1] + bps[2] * option[2] + bps[4] * option[3],
# 			bps[3] * option[2],
# 			bps[5] * option[3],
# 			0
# 			])
# 	temp_val = step(temp_m + 1, temp_storage - cost, rates.copy(), option, bps) > m
# 	if temp_val > mx:
# 		mx = temp_val

# 	return mx

	# Update storage

	# # Recurse
	# mx = 0
	# for option in options:
	# 	cost = np.array([
	# 		bps[0] * option[0] + bps[1] * option[1] + bps[2] * option[2] + bps[4] * option[3],
	# 		bps[3] * option[2],
	# 		bps[5] * option[3],
	# 		0
	# 		])

	# 	new_storage = step(m + 1, storage.copy() - cost, rates.copy(), option, bps, mx)
	# 	if new_storage > mx:
	# 		mx = new_storage
	# return mx


def dfs(t, recipes, storage, robots, cache):
	if t == 0:
		return storage[3]

	if (t, robots, storage) in cache:
		return cache[(t, robots, storage)]

	for i in range(4):
		storage[i] += robots[i]

	mx = 0
	for i in range(4):
		recipe = recipes[i]
		n = 0
		for j in range(4):
			if recipe[j] > 0 and robots[j] > 0:
				n = max(n, recipe[j] - storage[i] // robots[i]) 



def main():
	with open('test.txt', 'r') as f:
		data = f.read()

		nums = [int(a) for a in re.findall('[0-9]+', data)]
		bps = [np.array(nums[x + 1: x + 7]) for x in range(0, len(nums), 7)]

		rates = np.array([1, 0, 0, 0])
		storage = np.array([0, 0, 0, 0])
		queue = np.array([0, 0, 0, 0])

		print([step(0, storage, rates, queue, bp) for bp in bps])

if __name__ == "__main__":
	main()