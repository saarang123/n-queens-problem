import argparse
import random
from math import exp

DEC_RATE = 0.99
TEMPERATURE = 5000

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--n", type=int, default=8, help="number of queens")
args = vars(parser.parse_args())

n = args["n"]

max_fit = n * (n - 1) / 2

print("Number of queens: %d" % n)

def random_state():
	board = [i for i in range(n)]
	random.shuffle(board)
	return board

def fitness(state):
	cnt = 0
	for i in range(n):
		for x in range(i + 1, n):
			j = state[i]
			y = state[x]

			if j == y or i == x or (abs(y - j) == abs(x - i)):
				cnt += 1
	return max_fit - cnt

def random_next(state):
	while True:
		i = random.randint(0, n - 1)
		j = random.randint(0, n - 1)
		if i != j:
			break
	state[i], state[j] = state[j], state[i]
	return state

def simulated_annealing(output = False):
	current = random_state()

	t = TEMPERATURE
	iterations = 0
	while t > 0:
		t *= DEC_RATE
		fit = fitness(current)

		if fit == max_fit:
			break

		if output and iterations % 50 == 0:
			print("Iteration: %d" % iterations)
			print("Current Fitness: %d" % fit)
			print()

		successor = random_next(current)
		delta = fitness(successor) - fit

		if delta > 0:
			current = successor
		elif random.random() < exp(delta / t):
			current = successor
		iterations += 1

	solution = None

	if fitness(current) == max_fit:
		solution = current

	if solution == None:
		print()
		print("No solution found in specified iterations!")

	print()
	board = []
	for i in range(n):
		board.append(["."] * n)
	for i in range(n):
		board[solution[i]][i] = 'Q'

	print("Solution found!")
	for row in board:
		print(' '.join(row))

if __name__ == "__main__":
	simulated_annealing()