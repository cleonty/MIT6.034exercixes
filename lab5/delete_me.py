from itertools import combinations

a = [1, 2, 3, 4]

for p in combinations(a, 2):
	print list(p)
