import argparse
import random

MUTATE_PROB = 0.1
POPULATION_SIZE = 500
MAX_ITER = 5000

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--n", type=int, default=8, help="number of queens")
args = vars(parser.parse_args())

n = args["n"]

max_fit = n * (n - 1) / 2

print("Number of queens: %d" % n)

def random_state():
	return [random.randint(0, n - 1) for i in range(n)]

def fitness(state):
	cnt = 0
	for i in range(n):
		for x in range(i + 1, n):
			j = state[i]
			y = state[x]

			if j == y or i == x or (abs(y - j) == abs(x - i)):
				cnt += 1
	return max_fit - cnt

def probability(state):
	return fitness(state) / max_fit

def random_selection(pop_prob):
	# rank selection method
	total_prob = sum(fit for fit, s in pop_prob)

	random_prob = random.uniform(0, total_prob)

	cur_sum = 0
	for fit, s in pop_prob:
		cur_sum += fit
		# print(cur_sum, random_prob)
		if cur_sum >= random_prob:
			return s
	assert(False)

def reproduce(s1, s2):
	cut = random.randint(0, n - 1)
	return s1[:cut] + s2[cut:]

def mutate(state):
	index = random.randint(0, n - 1)
	row = random.randint(0, n - 1)
	state[index] = row
	return state

def genetic_iteration(population):
	new_population = []

	probs = [probability(state) for state in population]
	pop_prob = [(probs[i], population[i]) for i in range(len(population))]
	sorted_pop = sorted(pop_prob)
	new_population += [sorted_pop[0][1], sorted_pop[-1][1]] # retaining best/worst gen

	for i in range(len(population)):
		par1 = random_selection(pop_prob)
		par2 = random_selection(pop_prob)
		child = reproduce(par1, par2)

		if random.random() < MUTATE_PROB:
			child = mutate(child)

		new_population.append(child)

		if fitness(child) == max_fit:
			break;
	return new_population

def genetic_algo(output = False):
	population = [random_state() for _ in range(POPULATION_SIZE)]
	fit_pop = [fitness(state) for state in population]

	generation = 1

	while (max_fit not in fit_pop) and (generation <= MAX_ITER):
		population = genetic_iteration(population)
		fit_pop = [fitness(state) for state in population]

		if output and generation % 50 == 0:
			print("Generation: %d" % generation)
			print("Maximum fitness: %d" % max(fit_pop))
			print("Minimum fitness: %d" % min(fit_pop))
			print()

		generation += 1

	solution = None
	for state in population:
		if fitness(state) == max_fit:
			solution = state
			break

	if solution == None:
		print()
		print("No solution found in 5000 iterations!")

	print()
	board = []
	for i in range(n):
		board.append(["."] * n)
	for i in range(n):
		board[solution[i]][i] = 'Q'

	print("Solution found in generation: %d" % generation)
	for row in board:
		print(' '.join(row))

if __name__ == "__main__":
	genetic_algo()