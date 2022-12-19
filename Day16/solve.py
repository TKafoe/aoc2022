import re
import itertools
import tkinter
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


class Valve:
	def __init__(self, label, flow_rate, tunnels):
		self.label = label
		self.flow_rate = flow_rate
		self.tunnels = tunnels
		self.opened = False

	def open(self):
		self.opened = True

	def close(self):
		self.opened = False

def step_with_elephant(
	minute_p, 
	valve_p, 
	minute_e, 
	valve_e, 
	seen,
	val,
	distances,
	valves, 
	pressured_valves
	):
	if minute_p == 26 and minute_e == 26:
		return val

	options = pressured_valves.difference(seen)

	mx = 0
	i = 0
	no_options = True
	for option in options:
		seen.add(option)
		if not (minute_p + distances[valve_p][option] + 1 > 26):
			new_time_p = minute_p + distances[valve_p][option] + 1
			new_val = val + (26 - new_time_p) * valves[option].flow_rate
			new_mx = step_with_elephant(new_time_p, option, minute_e, valve_e, seen, new_val, distances, valves, pressured_valves)
			no_options = False
			if new_mx > mx:
				mx = new_mx

		if not (minute_e + distances[valve_e][option] + 1 > 26):
			new_time_e = minute_e + distances[valve_e][option] + 1
			new_val = val + (26 - new_time_e) * valves[option].flow_rate
			new_mx = step_with_elephant(minute_p, valve_p, new_time_e, option, seen, new_val, distances, valves, pressured_valves)
			no_options = False
			if new_mx > mx:
				mx = new_mx
		seen.remove(option)

		i += 1
		if len(seen) == 1:
			print(i)

	if no_options:
		return val
	return mx

def step(minute, valve, val, distances, valves, pressured_valves, path, paths, banned=set()):
	if len(path) >= len(pressured_valves)//2:
		return val
	if minute == 26:
		return val

	mx = 0
	no_options = True
	for next_valve in distances[valve]:
		if next_valve in banned or next_valve in path or next_valve == valve or minute + distances[valve][next_valve] + 1 > 26:
			continue

		no_options = False
		new_time = minute + distances[valve][next_valve] + 1
		new_val = val + (26 - new_time) * valves[next_valve].flow_rate
		paths.append([new_val, set(path + [next_valve])])
		new_mx = step(new_time, next_valve, new_val, distances, valves, pressured_valves, path + [next_valve], paths, banned)
		if new_mx > mx:
			mx = new_mx

	if no_options:
		return val
	return mx

def dijkstra(start_vertex, valves):
        D = {}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, PrioritizedItem(0, start_vertex)))
        visited = set()
        while not pq.empty():
                (dist, data) = pq.get()
                current_vertex = data.item
                visited.add(current_vertex)

                for neighbor in valves[current_vertex].tunnels:
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
	valves = {}
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		for row in data:
			label = row[6:8]
			flow_rate = int(re.search(r'\d+', row).group())
			tunnels = row.split("valves ")
			if len(tunnels) == 1:
				tunnels = [row.split("valve ")[1]]
			else:
				tunnels = tunnels[1].split(", ")

			valves[label] = Valve(label, flow_rate, tunnels)

	pressured_valves = list(filter(lambda x: valves[x].flow_rate > 0 or x == "AA", valves))
	distances = {}
	for v in pressured_valves:
		distances[v] = dijkstra(v, valves)
		for key in list(distances[v].keys()):
			if key not in pressured_valves:
				distances[v].pop(key)

	paths = []
	# print(distances)
	# print({key:valves[key].flow_rate for key in valves})
	# print(valves)
	val = step(0, "AA", 0, distances, valves, pressured_valves, ["AA"], paths)
	print(paths)

	mx = 0
	for i in range(0, len(paths)):
		for j in range(i, len(paths)):
			if paths[i][0] + paths[j][0] <= mx:
				continue
			if len(paths[i][1].difference(paths[j][1])) == 0 and paths[i][0] + paths[j][0] > mx:
				mx = paths[i][0] + paths[j][0]
	print(mx)


	# with open('input_dump.txt', 'w') as w:
	# 	for path in paths:
	# 		w.write(str(path) + "\n")
	# val = step_with_elephant(0, "AA", 0, "AA", set(["AA"]), 0, distances, valves, set(pressured_valves))
	# print(val)

if __name__ == "__main__":
	main()