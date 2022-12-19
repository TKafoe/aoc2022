class File:
	def __init__(self, size, parent, label):
		self.parent = parent
		self.size = size
		self.label = label

class Node:
	def __init__(self, parent, label):
		self.label = label
		self.parent = parent
		self.children = []
		self.size = 0

	def add_child(self, child):
		self.children.append(child)

	def remove_child(self, child):
		self.children.pop(child)

	def child_exists(self, label):
		return label in [c.label for c in self.children]

	def get_child(self, label):
		return next(child for child in self.children if child.label == label) 

class FileTree:
	def __init__(self, data):
		self.root = Node(None, "/")
		self.focused_node = self.root
		self.generate(data)

	def generate(self, data):
		for cmd in data:
			self.handle_cmd(cmd)

	def handle_cmd(self, cmd):
		cmd_split = cmd.split(" ")
		if cmd_split[0] == "$":
			if cmd_split[1] == "cd":
				label = cmd_split[2]
				if label == "/":
					self.focused_node = self.root
				elif label == "..":
					self.focused_node = self.focused_node.parent
				elif self.focused_node.child_exists(label):
					self.focused_node = self.focused_node.get_child(label)
				else:
					new_node = Node(self.focused_node, label)
					self.focused_node.add_child(new_node)
					self.focused_node = new_node
		elif cmd_split[0] != "dir":
			size = int(cmd_split[0])
			label = cmd_split[1]
			self.focused_node.add_child(File(size, self.focused_node, label))

	def get_size(self):
		files = []
		self.get_size_per_label(self.root, files)
		return files

	def get_size_per_label(self, node, files):
		if isinstance(node, File):
			files.append(("f/"+node.label, node.size))
			return node.size

		s = 0
		for child in node.children:
			s += self.get_size_per_label(child, files)

		files.append(("d/"+node.label, s))
		node.size = s
		return s

	def __str__(self):
		return self.pretty_print(self.root, 0)

	def pretty_print(self, node, depth):
		if isinstance(node, File):
			return "\t"*depth + "{} - {}\n".format(node.label, node.size)

		s = "\t"*depth + "{} - {}\n".format(node.label, node.size)
		for child in node.children:
			s += self.pretty_print(child, depth + 1)
		return s


with open('input.txt', 'r') as f:
	data = f.read().splitlines()
	tree = FileTree(data)
	sizes = tree.get_size()
	sorted_dirs = [v for v in sorted(sizes, key=lambda x: x[1], reverse=True) if v[0][0:2] == "d/"]
	print(sum([y[1] for y in filter(lambda x: x[1] <= 100000, sorted_dirs)]))

	total_size = sorted_dirs[0][1]
	unused_space = 70000000 - total_size
	needed_to_remove = 30000000 - unused_space
	print(needed_to_remove)
	print(min([x[1] for x in sorted_dirs if x[1] >= needed_to_remove]))

	print(tree)
