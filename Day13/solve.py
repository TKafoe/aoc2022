import json
import functools

def compare(m1, m2):
	if type(m1) == int and type(m2) == int:
		if m2 < m1:
			return False
		if m1 < m2:
			return True
		return None
	if type(m1) == list and type(m2) == int:
		return compare(m1, [m2])
	if type(m1) == int and type(m2) == list:
		return compare([m1], m2)
	if type(m1) == list and type(m2) == list:
		i = 0
		while i < len(m1) and i < len(m2):
			el1 = m1[i]
			el2 = m2[i]
			comp = compare(el1, el2)
			if not compare(el1, el2) == None:
				return comp
			i += 1
		if len(m1) > i and len(m2) == i:
			return False
		if len(m1) == i and len(m2) > i:
			return True
		return None

def comp_func(el1, el2):
	comp = compare(el1, el2)
	if comp == True:
		return 1
	if comp == False:
		return -1
	if comp == None:
		return 0

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()

		s = 0
		packets = []
		for i in range(0, len(data), 3):
			ar1 = json.loads(data[i])
			ar2 = json.loads(data[i+1])
			packets.append(ar1)
			packets.append(ar2)
			if compare(ar1, ar2):
				s += (i // 3) + 1
		print(s)
		packets.append([[2]])
		packets.append([[6]])

		sor = sorted(packets, key=functools.cmp_to_key(comp_func), reverse=True)
		print((sor.index([[2]])+ 1) * (sor.index([[6]]) + 1))
if __name__ == "__main__":
	main()