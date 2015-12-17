# Z13
z13 = range(2,12)
gens = 0
for i in z13:
	gen = [i**n%13 for n in range(12)]
	print gen
	freq = sum([i for i in gen if i == 1])
	if freq == 1:
		gens += 1 
print gens
