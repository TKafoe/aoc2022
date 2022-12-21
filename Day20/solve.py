class Node:
	def __init__(self, val):
		self.val = val
		self.prev = None
		self.next = None

	def connect(self, node):
		self.next = node
		node.prev = self

	def move(self, steps):
		if steps < 0:
			self.move_backwards(abs(steps))
		else:
			self.move_forwards(steps)

	def move_backwards(self, steps):
		while steps > 0:
			pp = self.prev.prev
			self.prev.connect(self.next)
			self.connect(self.prev)
			pp.connect(self)
			steps -= 1

	def move_forwards(self, steps):
		while steps > 0:
			nn = self.next.next
			self.prev.connect(self.next)
			self.next.connect(self)
			self.connect(nn)
			steps -= 1

	def __str__(self):
		s = "{}".format(self.val)
		n = self.next
		while n != self:
			s += " {} ".format(n.val)
			n = n.next
		return s

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()

		num = 811589153

		nodes = {}

		v = int(data[0]) * num
		ll = Node(v)
		nodes[0] = (abs(ll.val) % (len(data) - 1), ll)
		if v < 0:
			nodes[0] = (-1 * nodes[0][0], ll)

		node_0 = None
		temp_node = ll
		for i in range(1, len(data)):
			v = int(data[i]) * num
			nn = Node(v)
			nodes[i] = (abs(v) % (len(data) - 1), nn)
			if v < 0:
				nodes[i] = (-1 * nodes[i][0], nn)
			if nn.val == 0:
				node_0 = nn

			temp_node.connect(nn)
			temp_node = nn
		temp_node.connect(ll)

		for _ in range(10):
			for i in range(0, len(data)):
				v, node = nodes[i]
				if v == 0:
					continue

				node.move(v)

		node = node_0
		s = 0
		n = 0
		while n <= 3000:
			if n == 1000:
				s += node.val
			if n == 2000:
				s += node.val
			if n == 3000:
				s += node.val

			node = node.next
			n += 1

		print(s)
if __name__ == "__main__":
	main()