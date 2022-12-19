with open('input.txt', 'r') as f:
	data = f.read().splitlines()

	CRT = [["0" for _ in range(40)] for _ in range(6)]
	print(CRT)

	s = 0
	cycle = 1
	X = 1
	for ex in data:
		if ex == "noop":
			if (cycle + 20) % 40 == 0:
				s += cycle * X

			CRT[(cycle - 1) // 40][(cycle - 1) % 40] = "#" if abs(X - ((cycle - 1) % 40)) <= 1 else "."
			cycle += 1
		else:
			cmd = ex.split(" ")
			for _ in range(2):
				if (cycle + 20) % 40 == 0:
					s += cycle * X

				CRT[(cycle - 1) // 40][(cycle - 1) % 40] = "#" if abs(X - ((cycle - 1) % 40)) <= 1 else "."
				cycle += 1
			X += int(cmd[1])

	print(s)
	for st in CRT:
		print(st)

