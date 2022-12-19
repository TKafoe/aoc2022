import math

class Monkey:
	def __init__(self, start_items, operation, operation_val, test, m1, m2):
		self.items = start_items
		self.operation = operation
		self.operation_val = int(operation_val) if operation_val != "old" else "old"
		self.test = test
		self.m1 = m1
		self.m2 = m2
		self.inspected = 0

	def round(self, monkeys, lcm, worry_reduction):
		while len(self.items) > 0:
			self.inspect(self.items.pop(0), monkeys, lcm, worry_reduction)

	def inspect(self, item, monkeys, lcm, worry_reduction):
		self.inspected += 1
		if self.operation == "+":
			item += self.operation_val
		else:
			item *= self.operation_val if self.operation_val != "old" else item

		if worry_reduction:
			item //= worry_reduction
		if lcm:
			item %= lcm

		if item % self.test == 0:
			monkeys[self.m1].receive(item)
		else:
			monkeys[self.m2].receive(item)

	def receive(self, item):
		self.items.append(item)

def init_monkeys(data):
	monkeys = []
	for i in range(0, len(data), 7):
		items = [int(x) for x in data[i + 1][18:].split(", ")]
		operation = data[i + 2][23:24]
		operation_val = data[i + 2][25:]
		test = int(data[i + 3][21:])
		m1 = int(data[i + 4][29:])
		m2 = int(data[i + 5][30:])
		monkeys.append(Monkey(items, operation, operation_val, test, m1, m2))
	return monkeys

def do(data, rounds, worry_reduction=0, use_lcm=False):
		monkeys = init_monkeys(data)
		lcm = math.lcm(*[m.test for m in monkeys])
		for i in range(rounds):
			for monkey in monkeys:
				monkey.round(monkeys, lcm if use_lcm else 0, worry_reduction)
		sort = sorted([m.inspected for m in monkeys], reverse=True)
		print(sort[0] * sort[1])

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		do(data, 20, worry_reduction=3, use_lcm=False)
		do(data, 10000, worry_reduction=0, use_lcm=True)

if __name__ == "__main__":
	main()