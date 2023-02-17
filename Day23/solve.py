def print_elves(elves, padding=2):
	minx = 2_000_000
	maxx = -2_000_000
	miny = 2_000_000
	maxy = -2_000_000

	for elf in elves:
		if elf[0] > maxx:
			maxx = elf[0]
		if elf[0] < minx:
			minx = elf[0]
		if elf[1] > maxy:
			maxy = elf[1]
		if elf[1] < miny:
			miny = elf[1]

	xrang = maxx - minx

	for j in range(maxy + padding):
		s = ""
		for i in range(maxx + padding):
			if (i, j) in elves:
				s += "#"
			else:
				s += "."
		print(s)

def propose_elf(elf, elves, round_i):
	adj_m = [
	[(elf[0] - 1, elf[1] - 1) in elves, 
		(elf[0], elf[1] - 1) in elves,
			(elf[0] + 1, elf[1] - 1) in elves],
	[(elf[0] - 1, elf[1]) in elves, 
		False,
			(elf[0] + 1, elf[1]) in elves],
	[(elf[0] - 1, elf[1] + 1) in elves, 
		(elf[0], elf[1] + 1) in elves,
			(elf[0] + 1, elf[1] + 1) in elves]
	]

	if not any([any(l) for l in adj_m]):
		return elf

	if round_i % 4 == 0:
		if not any(adj_m[0]):
			return (elf[0], elf[1] - 1)
		if not any(adj_m[2]):
			return (elf[0], elf[1] + 1)
		if not (adj_m[0][0] or adj_m[1][0] or adj_m[2][0]):
			return (elf[0] - 1, elf[1])
		if not (adj_m[0][2] or adj_m[1][2] or adj_m[2][2]):
			return (elf[0] + 1, elf[1])
	elif round_i % 4 == 1:
		if not any(adj_m[2]):
			return (elf[0], elf[1] + 1)
		if not (adj_m[0][0] or adj_m[1][0] or adj_m[2][0]):
			return (elf[0] - 1, elf[1])
		if not (adj_m[0][2] or adj_m[1][2] or adj_m[2][2]):
			return (elf[0] + 1, elf[1])
		if not any(adj_m[0]):
			return (elf[0], elf[1] - 1)
	if round_i % 4 == 2:
		if not (adj_m[0][0] or adj_m[1][0] or adj_m[2][0]):
			return (elf[0] - 1, elf[1])
		if not (adj_m[0][2] or adj_m[1][2] or adj_m[2][2]):
			return (elf[0] + 1, elf[1])
		if not any(adj_m[0]):
			return (elf[0], elf[1] - 1)
		if not any(adj_m[2]):
			return (elf[0], elf[1] + 1)
	if round_i % 4 == 3:
		if not (adj_m[0][2] or adj_m[1][2] or adj_m[2][2]):
			return (elf[0] + 1, elf[1])
		if not any(adj_m[0]):
			return (elf[0], elf[1] - 1)
		if not any(adj_m[2]):
			return (elf[0], elf[1] + 1)
		if not (adj_m[0][0] or adj_m[1][0] or adj_m[2][0]):
			return (elf[0] - 1, elf[1])

	return elf

def do_round(elves, round_i):
	proposed_steps = {}
	banned = set()
	for elf in elves:
		proposed_step = propose_elf(elf, elves, round_i)
		if proposed_step == elf or proposed_step in banned:
			continue
		if proposed_step not in proposed_steps:
			proposed_steps[proposed_step] = elf
		else:
			del proposed_steps[proposed_step]
			banned.add(proposed_step)

	if len(proposed_steps.keys()) == 0:
		return elves.difference(set(proposed_steps.values())).union(set(proposed_steps.keys())), True

	return elves.difference(set(proposed_steps.values())).union(set(proposed_steps.keys())), False

def do(elves):
	i = 0
	while True:
		elves, res = do_round(elves, i)
		if res:
			print(i + 1)
			break
		i+=1

	return elves


def find_empty_tiles(elves):
	minx = 2_000_000
	maxx = -2_000_000
	miny = 2_000_000
	maxy = -2_000_000

	for elf in elves:
		if elf[0] > maxx:
			maxx = elf[0]
		if elf[0] < minx:
			minx = elf[0]
		if elf[1] > maxy:
			maxy = elf[1]
		if elf[1] < miny:
			miny = elf[1]

	edge1 = maxx - minx + 1
	edge2 = maxy - miny + 1

	return edge1 * edge2 - len(elves)

def main():
	with open('input.txt', 'r') as f:
		data = f.readlines()
		elves = set()
		for i, row in enumerate(data):
			for j, s in enumerate(row):
				if s == "#":
					elves.add((j, i))

		elves = do(elves)
		print(find_empty_tiles(elves))

if __name__ == "__main__":
	main()