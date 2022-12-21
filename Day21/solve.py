def evaluate(s, vrs):
	if type(vrs[s]) == int:
		return vrs[s]

	v1 = evaluate(vrs[s][0], vrs)
	v2 = evaluate(vrs[s][2], vrs)

	op = vrs[s][1]
	if op == "+":
		return v1 + v2
	elif op == "-":
		return v1 - v2
	elif op == "/":
		return v1 / v2
	else:
		return v1 * v2

def evaluate_str(s, vrs):
	if s == "humn":
		return (1, 0)

	if type(vrs[s]) == int:
		return (0, vrs[s])

	v1 = evaluate_str(vrs[s][0], vrs)
	v2 = evaluate_str(vrs[s][2], vrs)

	op = vrs[s][1]
	if op == "+":
		return (v1[0] + v2[0], v1[1] + v2[1])
	elif op == "-":
		return (v1[0] - v2[0], v1[1] - v2[1])
	elif op == "/":
		if v2[1] == 0:
			return (0, 0)
		return (v1[0] / v2[1], v1[1] / v2[1])
	else:
		return (v1[0] * v2[1] + v1[1] * v2[0], v1[1] * v2[1])

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()

		vrs = {}
		for row in data:
			if len(row.split(" ")) > 2:
				vrs[row[0:4]] = row[6:].split(" ")
			else:
				vrs[row[0:4]] = int(row.split(" ")[1])

		print(int(evaluate("root", vrs)))
		f1 = evaluate_str(vrs["root"][0], vrs)
		f2 = evaluate_str(vrs["root"][2], vrs)

		a = f1[0]
		b = f1[1]
		c = f2[0]
		d = f2[1]
		print(int((d - b) / (a - c)))

if __name__ == "__main__":
	main()