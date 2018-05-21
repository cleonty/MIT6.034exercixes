from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain, simplify

theft_rule = IF( 'you have (?x)', THEN( 'i have (?x)'), DELETE( 'you have (?x)'))
data = ('you have apple', 'you have orange', 'you have pear', 'i have pear', 'i have apple')

print forward_chain([theft_rule], data, verbose=False)

print simplify(AND('g', 'g', 'g'))
print simplify(AND('g1', AND('g2', AND('g3', AND('g4', AND())))))


a = [1, [2,3]]

for i in xrange(len(a)):
	a[i] = 5
print a

print *[1,2,3]