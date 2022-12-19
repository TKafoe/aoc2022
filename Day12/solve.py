import string
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

def check_connected(graph, h1, i, j):
	return (0 <= i and i < len(graph) and 0 <= j and j < len(graph[i])) \
			and (h1 >= graph[i][j].height or graph[i][j].height - h1 == 1)

class Node:
	def __init__(self, height):
		self.height = height
		self.edges = set()

	def connect(self, node):
		self.edges.add(node)

def build_graph(data):
	end = None
	start = None
	graph = []
	for i in range(len(data)):
		r = []
		for j in range(len(data[i])):
			node = None
			if data[i][j] == "E":
				node = Node(string.ascii_lowercase.index("z"))
				end = node
			elif data[i][j] == "S":
				node = Node(string.ascii_lowercase.index("a"))
				start = node
			else:
				node = Node(string.ascii_lowercase.index(data[i][j]))
			r.append(node)
		graph.append(r)

	for i in range(len(graph)):
		for j in range(len(data[i])):
			node = graph[i][j]
			if check_connected(graph, node.height, i + 1, j):
				node.connect(graph[i + 1][j])
			if check_connected(graph, node.height, i - 1, j):
				node.connect(graph[i - 1][j])
			if check_connected(graph, node.height, i, j + 1):
				node.connect(graph[i][j + 1])
			if check_connected(graph, node.height, i, j - 1):
				node.connect(graph[i][j - 1])

	return start, end, graph

def dijkstra(start_vertex):
	D = {}
	D[start_vertex] = 0

	pq = PriorityQueue()
	pq.put((0, PrioritizedItem(0, start_vertex)))
	visited = set()
	while not pq.empty():
		(dist, data) = pq.get()
		current_vertex = data.item
		visited.add(current_vertex)

		for neighbor in current_vertex.edges:
			if neighbor not in visited:
				if neighbor not in D:
					D[neighbor] = float('inf')
				old_cost = D[neighbor]
				new_cost = D[current_vertex] + 1
				if new_cost < old_cost:
					pq.put((new_cost, PrioritizedItem(new_cost, neighbor)))
					D[neighbor] = new_cost
	return D

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()

		start, end, graph = build_graph(data)
		D = dijkstra(start)
		print(D[end])

		mx = float('inf')
		for row in graph:
			node = row[0]
			if node.height == 0:
				D = dijkstra(node)
				if end in D and D[end] < mx:
					mx = D[end]

		print(mx)


if __name__ == "__main__":
	main()