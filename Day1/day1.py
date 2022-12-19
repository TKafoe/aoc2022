with open('input.txt', 'r') as f:
	data = f.read().splitlines()
	
	subtotals = []
	subtotal = 0
	for cal in data:
		if cal == "":
			subtotals.append(subtotal)
			subtotal = 0
		else:
			subtotal += int(cal)

	print(sum(sorted(subtotals, reverse=True)[:3]))
