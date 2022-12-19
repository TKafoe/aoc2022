SCORES = {
	"A X": 3,
	"A Y": 1 + 3,
	"A Z": 2 + 6,
	"B X": 1,
	"B Y": 2 + 3,
	"B Z": 3 + 6,
	"C X": 2,
	"C Y": 3 + 3,
	"C Z": 1 + 6
}

with open('input.txt', 'r') as f:
	data = f.read().splitlines()
	score = 0
	for d in data:
		score += SCORES[d]

	print(score)