import math

R = 1120
R_i = 1120 + math.ceil(R / 0.977) * 0.443
while R < R_i:
	R = R_i
	R_i = 1120 + math.ceil(R / 0.977) * 0.443
	print("\t \\item {}".format(R_i))

print(R_i)