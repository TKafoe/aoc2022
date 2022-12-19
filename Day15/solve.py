import re

class Sensor:
	def __init__(self, sensor, beacon):
		self.sensor = sensor
		self.beacon = beacon
		self.manh_dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

	def get_no_beacon_points(self, i):
		dist = abs(self.sensor[1] - i)
		points = set()
		if dist > self.manh_dist:
			return points

		s = -(self.manh_dist - dist)
		while s <= self.manh_dist - dist:
			points.add(self.sensor[0] + s)
			s += 1

		return points

	def point_known(self, p):
		known = (abs(self.sensor[0] - p[0]) + abs(self.sensor[1] - p[1])) <= self.manh_dist
		if not known:
			return known, -1

		dist = self.manh_dist - abs(self.sensor[1] - p[1])
		size = 2*(dist) + 1
		offset = p[0] - (self.sensor[0] - dist)
		return known, size - offset


def get_no_beacon_points_from_sensors(sensors, i):
	points = set()
	beacons = set()
	for sensor in sensors:
		points = points.union(sensor.get_no_beacon_points(i))
		if sensor.beacon[1] == i:
			beacons.add(sensor.beacon[0])

	return points.difference(beacons)

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		sensors = []
		for row in data:
			values = [int(x) for x in re.findall(r'-?\d+', row)]
			sensors.append(Sensor((values[0], values[1]), (values[2], values[3])))

		# nb_points = get_no_beacon_points_from_sensors(sensors, 2000000)
		# # print(sorted(list(nb_points)))
		# print(len(nb_points))

		sensors = sorted(sensors, key=lambda x: x.manh_dist, reverse=True)
		y = 0
		Found = False
		while y < 4000000 and not Found:
			x = 0
			while x < 4000000 and not Found:
				for sensor in sensors:
					in_sensor, dist = sensor.point_known((x, y))
					if in_sensor:
						x += dist
						break
				else:
					print((x,y))
					print(x * 4000000 + y)
					Found = True
			y += 1

if __name__ == "__main__":
	main()

