

lines = []

with open('./pb4/input6.txt', 'r') as inputs:
    for line in inputs:
    	lines.append(line.rstrip())

N = int(lines[0])
strands = lines[1:]

possibles = {'A' : 'T', 'T': 'A', 'C' : 'G', 'G' : 'C'}

com = {}

for i, strand in enumerate(strands):
	com.update({strand : []})
	
	possible_strand = ''
	for acide in strand:
		for key in possibles.keys():
			if acide == key:
				possible_strand += possibles[key]
	com[strand]=possible_strand

count = 0
for i, strand in enumerate(strands):
	count += len(strand)

middle = count / 2


l_split = {'left':[], 'right' : []}

s = strands.pop(0)
l_split['left'].append(s)

l_strand = len(s)

impossibles = {'left' : [], 'right' : []}

for c in com.items():
			if c[0] == s:
				impossibles['left'].append(c[1])


for i, strand in enumerate(strands):
	if len(strand) + l_strand > middle or strand in impossibles['left']:
		continue
	else:
		for c in com.items():
			if c[0] == strand:
				impossibles['left'].append(c[1])
			
		l_strand += len(strand)
		l_split['left'].append(strands.pop(i))

l_split['right'] = strands

strand_right = []
strand_left = []
order_right = []

for accide_left in l_split['left']:
	order_right.append(com[accide_left])

def create_perm(n):
	L = [[0]]
	for i in range(1, n):
		L_new = []
		for p in L:
			for pos in range(len(p)+1):
				p_new = p[:pos] + [i] + p[pos:]
				L_new.append(p_new)
		L = L_new
	return L

strand_right = l_split['right'] 
strand_left = l_split['left']
l_right = len(strand_right)
permutation_right = create_perm(l_right)

comb_right = []
for permutation in permutation_right:
	sub_comb = []
	for pos in permutation:
			sub_comb.append(strand_right[pos])
	
	comb_right.append(sub_comb)


solution_left = "".join(order_right)

for i, crp in enumerate(comb_right):
	if solution_left == "".join(crp):
		break

strand_left.reverse()
possible = " ".join(strand_left) + "#" + " ".join(comb_right[i])

print(possible)