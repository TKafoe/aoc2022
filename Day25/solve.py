def dec_to_base(num, base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base
    base_num = base_num[::-1]  #To reverse the string
    return base_num

def to_snafu(val):
	lval = [int(x) for x in list(dec_to_base(val, 5))][::-1]

	for i, val in enumerate(lval):
		if val == 3:
			if i == len(lval) - 1:
				lval.append(0)
			lval[i + 1] += 1
			lval[i] -= 5
		if val == 4:
			if i == len(lval) - 1:
				lval.append(0)
			lval[i + 1] += 1
			lval[i] -= 5

	for i, val in enumerate(lval):
		if val == 5:
			lval[i] = 0
			if i == len(lval) - 1:
				lval.append(0)
			lval[i + 1] += 1

	return "".join([str(i) for i in lval[::-1]]).replace("-2", "=").replace("-1", "-")

def from_snafu(snafu_val):
	sm = 0
	for i, dig in enumerate(snafu_val[::-1]):
		if dig == "=":
			sm += 5**i * -2
		elif dig == "-":
			sm += 5**i * -1
		else:
			sm += 5**i * int(dig)
	return int(sm)

def main():
	with open('input.txt', 'r') as f:
		data = f.read().splitlines()
		
		print(to_snafu(sum([from_snafu(snafu_num) for snafu_num in data])))


if __name__ == "__main__":
	main()