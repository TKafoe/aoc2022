import re
import math

def dfs(t, recipes, storage, robots, cache, max_spend_rates):
	if t == 0:
		cache[(t, str(robots), str(storage))] = storage[3]
		return storage[3]

	if (t, str(robots), str(storage)) in cache:
		return cache[(t, str(robots), str(storage))]

	mx = 0
	for robot in range(4):
		if robot < 3 and max_spend_rates[robot] <= robots[robot]:
			continue
		recipe = recipes[robot]
		n = 0
		can_be_made = True
		for ore in range(3):
			if recipe[ore] > 0: 
				if robots[ore] == 0:
					can_be_made = False
					break
				else:
					n = max(n, math.ceil((recipe[ore] - storage[ore]) / robots[ore]))
		if can_be_made:
			n += 1
			if t - n > 0:
				storage_copy = storage[:]
				for i in range(4):
					storage_copy[i] += robots[i] * n
					storage_copy[i] -= recipe[i]
					if i < 3:
						storage_copy[i] = min(storage_copy[i], max_spend_rates[i] * (t - n))

				robots_copy = robots[:]
				robots_copy[robot] += 1
				mx = max(mx, dfs(t - n, recipes, storage_copy, robots_copy, cache, max_spend_rates))

	storage_copy = storage[:]
	for i in range(4):
		if i < 3:
			storage_copy[i] = 0
		else:
			storage_copy[i] += robots[i] * t
	mx = max(mx, dfs(0, recipes, storage_copy, robots, cache, max_spend_rates))

	cache[(t, str(robots), str(storage))] = mx
	return mx

def main():
	with open('input.txt', 'r') as f:
		data = f.read()

		nums = [int(a) for a in re.findall('[0-9]+', data)]
		bps = [nums[x + 1: x + 7] for x in range(0, len(nums), 7)]
		recipes = [[[r[0], 0, 0, 0], [r[1], 0, 0, 0], [r[2], r[3], 0, 0], [r[4], 0, r[5], 0]] for r in bps][0:3]
		max_spend_rates = [[max([recipe[i] for recipe in recipe_list]) for i in range(4)] for recipe_list in recipes]
		storage = [0, 0, 0, 0]
		robots = [1, 0, 0, 0]
		cache = {}
		s = 1
		for i, recipe in enumerate(recipes):
			print(i)
			s *= dfs(32, recipe, storage[:], robots[:], cache.copy(), max_spend_rates[i])
		print(s)

if __name__ == "__main__":
	main()