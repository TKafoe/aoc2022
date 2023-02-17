from queue import PriorityQueue
import queue
from dataclasses import dataclass, field
from typing import Any

def get_all_states(init_pos, init_i, states, goal):
	states_queue = queue.Queue()
	states_graph = {
		(init_pos, init_i): set()
	}
	states_queue.put((init_pos, init_i, 0))

	while not states_queue.empty():
		print(states_queue.qsize())
		pos, cur_state, time = states_queue.get()
		if pos == goal:
			return states_graph
		if time > 500:
			continue

		states_graph[(pos, cur_state)] = set()

		next_state = (cur_state + 1) % len(states)
		options = get_options(pos, states[next_state])

		for option in options:
			states_graph[(pos, cur_state)].add((option, next_state))
			if (option, next_state) in states_graph:
				continue
			states_queue.put((option, next_state, time + 1))

	return states_graph


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

def get_next_state(state):
	new_state = [[set() for i in range(len(state[j]))] for j in range(len(state))]

	for i in range(len(state)):
		for j in range(len(state[i])):
			for move in state[i][j]:
				if move == "<":
					new_state[i][(j - 1) % len(state[i])].add("<")
				if move == ">":
					new_state[i][(j + 1) % len(state[i])].add(">")
				if move == "^":
					new_state[(i - 1) % len(state)][j].add("^")
				if move == "v":
					new_state[(i + 1) % len(state)][j].add("v")
	return new_state

def state_equal(state1, state2):
	for i, row in enumerate(state1):
		for j, column in enumerate(state1[i]):
			if state1[i][j] != state2[i][j]:
				return False
	return True

def get_options(pos, state):
	options = set()
	x = pos[0]
	y = pos[1]
	if len(state[y][x]) == 0:
		options.add(pos)

	if x + 1 < len(state[y]) and len(state[y][x + 1]) == 0:
		options.add((x + 1, y))
	if x - 1 >= 0 and len(state[y][x - 1]) == 0:
		options.add((x - 1, y))
	if y + 1 < len(state) and len(state[y + 1][x]) == 0:
		options.add((x, y + 1))
	if y - 1 >= 0 and len(state[y - 1][x]) == 0:
		options.add((x, y - 1))

	return options

def print_state(pos, state):
	print()
	for i, row in enumerate(state):
		s = ""
		for j, el in enumerate(row):
			if (j, i) == pos:
				s += "P"
			elif len(el) > 1:
				s += "{}".format(len(el))
			elif len(el) == 0:
				s += "."
			else:
				s += "".join(el)
		print(s)
	print()


def bfs(start, goal, init_state, states):
	state_queue = queue.PriorityQueue()
	state_queue.put((
		abs(goal[0] - start[0] + goal[1] - start[1]), 
		PrioritizedItem(abs(goal[0] - start[0] + goal[1] - start[1]), (start, init_state, 0))
		))

	seen_states = set()
	found_routes = set()
	best = (-1, 2_000_000)
	while not state_queue.empty():
		(dist, data) = state_queue.get()
		cur_state = data.item

		if best[1] < cur_state[2]:
			continue

		if cur_state in seen_states:
			continue

		seen_states.add(cur_state)

		if goal == cur_state[0]:
			found_routes.add((cur_state[1], cur_state[2]))

		if goal == cur_state[0] and best[1] > cur_state[2]:
			best = (cur_state[1], cur_state[2])

		next_state = (cur_state[1] + 1) % len(states)
		options = get_options(cur_state[0], states[next_state])
		for option in options:
			state_queue.put((
				abs(goal[0] - option[0] + goal[1] - option[1]),
				PrioritizedItem(abs(goal[0] - option[0] + goal[1] - option[1]), (option, next_state, cur_state[2] + 1))
			))
	
	return best, found_routes

def get_offset(init_state, states, loc):
	s = (init_state + 1) % len(states)
	offset = 1
	while len(states[s][loc[1]][loc[0]]) != 0:
		s = (s + 1) % len(states)
		offset+=1

	return offset, s

def get_all_state_pos(state):
	all_states = [state]
	s = get_next_state(state)
	i = 0
	while s != state:
		all_states.append(s)
		i += 1
		s = get_next_state(s)

	return all_states

def dijkstra(start_vertex, graph):
	D = {}
	D[start_vertex] = 0

	pq = PriorityQueue()
	pq.put((0, PrioritizedItem(0, start_vertex)))
	visited = set()
	while not pq.empty():
		(dist, data) = pq.get()
		current_vertex = data.item
		visited.add(current_vertex)

		for neighbor in graph[current_vertex]:
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
		data = f.readlines()

		start = (0, 0)
		goal = (len(data[-1]) - 3, len(data) - 3)

		state = []
		for line in data[1:len(data) - 1]:
			l_state = []
			for c in line[1:len(line) - 2]:
				l_state.append(set())
				if c != ".":
					l_state[-1].add(c)
			state.append(l_state)

		all_states = get_all_state_pos(state)

		minutes_passed = 0
		offset, s = get_offset(0, all_states, start)
		minutes_passed += offset
		best_route, routes_found = bfs(start, goal, offset, all_states)
		minutes_passed += best_route[1] + 1
		best_one = minutes_passed
		print("Best one-way 1st route: {}".format(minutes_passed))

		offset, s = get_offset(minutes_passed, all_states, goal)
		minutes_passed += offset
		best_route, routes_found = bfs(goal, start, (minutes_passed) % len(all_states), all_states)
		while best_route[0] == -1:
			offset, s = get_offset(minutes_passed, all_states, goal)
			minutes_passed += offset
			best_route, routes_found = bfs(goal, start, (minutes_passed) % len(all_states), all_states)

		best_route, routes_found = bfs(goal, start, (minutes_passed) % len(all_states), all_states)
		minutes_passed += best_route[1] + 1
		print("Best one-way 2nd route: {}".format(minutes_passed - best_one))

		offset, s = get_offset(minutes_passed, all_states, start)
		minutes_passed += offset
		best_route, routes_found = bfs(start, goal, (minutes_passed) % len(all_states), all_states)
		while best_route[0] == -1:
			offset, s = get_offset(minutes_passed, all_states, start)
			minutes_passed += offset
			best_route, routes_found = bfs(start, goal, (minutes_passed) % len(all_states), all_states)

		best_route, routes_found = bfs(start, goal, (minutes_passed) % len(all_states), all_states)
		minutes_passed += best_route[1] + 1
		print("Best one-way 3nd route: {}".format(minutes_passed - best_one))

		print("Total time: {}".format(minutes_passed))

if __name__ == "__main__":
	main()
