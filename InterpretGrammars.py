from progressbar import *
from sets import *
from itertools import *

grammars = {}
infile = open('Possible_Grammars.txt')
lines = infile.readlines()
widgets = ['Lines: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
           ' ', ETA(), ' ']
pbar = ProgressBar(widgets=widgets, maxval=len(lines)+1).start()
for i in range(len(lines)):
	line = lines[i]
	key = eval(line.split('@')[0])
	try:
		grammars[frozenset(key)] += [line.split('@')[1]]
	except:
		grammars[frozenset(key)] = [line.split('@')[1]]
	pbar.update(i)

pbar.finish()

possible_reflexes = {
'cut':['prVs','parVs'],
'G':[''],
'N':['na','n'],
'D':['an','n','na'],
'S':['sa','s'],
't1':['ta','t'],
't2':['ta','t'],
'tn':['tana','tan'],
'':[''],
'Preterite':[''],
'Durrative':['na','an','n'],
'3sg':['V']
}

#Initial Test for Compatibility
outfile = open('ResultsForReflexes.txt','w')
for key in possible_reflexes:
	for reflex in possible_reflexes[key]:
		print key + ':' + reflex
		outfile.write(key + ':' + reflex + '\n')
		for key2 in grammars:
			if key in key2:
				numof = 0
				for item in grammars[key2]:
					if (key != 'cut') and (key + ':' + reflex + ',' in item):
						numof += 1
					elif (key == 'cut') and (key + ':' + reflex in item):
						numof += 1
				print '\t' + str(key2) + ': ' + str(numof)
				outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

#Exclude all grammars which have, since they cannot generate some forms:
# cut:prVs
# S:s
# tn:tana
# Durrative:na

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		if ('cut:prVs' not in item) and ('S:s,' not in item) and ('tn:tana,' not in item) and ('Durrative:na,' not in item):
			try:
				newgrammars[key] += [item]
			except:
				newgrammars[key] = [item]

grammars = newgrammars

possible_reflexes = {
'cut':['parVs'],
'G':[''],
'N':['na','n'],
'D':['an','n','na'],
'S':['sa'],
't1':['ta','t'],
't2':['ta','t'],
'tn':['tan'],
'':[''],
'Preterite':[''],
'Durrative':['an','n'],
'3sg':['V']
}

#Second round of elimination

outfile = open('ResultsForReflexesRound2.txt','w')
for key in possible_reflexes:
	for reflex in possible_reflexes[key]:
		print key + ':' + reflex
		outfile.write(key + ':' + reflex + '\n')
		for key2 in grammars:
			if key in key2:
				numof = 0
				for item in grammars[key2]:
					if (key != 'cut') and (key + ':' + reflex + ',' in item):
						numof += 1
					elif (key == 'cut') and (key + ':' + reflex in item):
						numof += 1
				print '\t' + str(key2) + ': ' + str(numof)
				outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

#Exclude all grammars which have, since they cannot generate some forms:
# N:n

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		if ('N:n,' not in item):
			try:
				newgrammars[key] += [item]
			except:
				newgrammars[key] = [item]

grammars = newgrammars

possible_reflexes = {
'cut':['parVs'],
'G':[''],
'N':['na'],
'D':['an','n','na'],
'S':['sa'],
't1':['ta','t'],
't2':['ta','t'],
'tn':['tan'],
'':[''],
'Preterite':[''],
'Durrative':['an','n'],
'3sg':['V']
}

#Third round of elimination

outfile = open('ResultsForReflexesRound3.txt','w')
for key in possible_reflexes:
	for reflex in possible_reflexes[key]:
		print key + ':' + reflex
		outfile.write(key + ':' + reflex + '\n')
		for key2 in grammars:
			if key in key2:
				numof = 0
				for item in grammars[key2]:
					if (key != 'cut') and (key + ':' + reflex + ',' in item):
						numof += 1
					elif (key == 'cut') and (key + ':' + reflex in item):
						numof += 1
				print '\t' + str(key2) + ': ' + str(numof)
				outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()


#Reset grammars to non-strings

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		try:
			newgrammars[key] += [eval(item)]
		except:
			newgrammars[key] = [eval(item)]

grammars = newgrammars
exponents = []
for key in grammars:
	for item in grammars[key]:
		for exponent in item[1]:
			if (exponent not in exponents) and (exponent not in ['Syncope', 'Nassim']):
				exponents.append(exponent)


#Start Syncope Testing

widgets = ['Keys: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
           ' ', ETA(), ' ']
pbar = ProgressBar(widgets=widgets, maxval=len(grammars.keys())+1).start()
exponents = []
for i in range(len(grammars.keys())):
	key = grammars.keys()[i]
	for item in grammars[key]:
		for exponent in item[1]:
			newex = exponent.split(',')[0]
			if (newex not in exponents) and (newex not in ['Syncope', 'Nassim']):
				exponents.append(newex)
	pbar.update(i)

pbar.finish()

#Check for Syncope Consistancy with each item
outfile = open('ResultsForSyncope.txt','w')
for exp in exponents:
	print str(exp) + '@No Syncope' 
	outfile.write(str(exp) + '@No Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] != 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')
	print str(exp) + '@Syncope' 
	outfile.write(str(exp) + '@Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] == 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')

outfile.close()

#Eliminate grammars without Syncope after 3sg and with Syncope after N

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		cont = True
		if True in ['N:' in x for x in item[1]]:
			index = ['N:' in x for x in item[1]].index(True)
			if 'Syncope' in item[1][index + 1]:
				cont = False
		if cont:
			index = ['3sg:' in x for x in item[1]].index(True)
			if 'Syncope' in item[1][index + 1]:
				try:
					newgrammars[key] += [item]
				except:
					newgrammars[key] = [item]	

grammars = newgrammars

#Check for Syncope Consistancy with each item
outfile = open('ResultsForSyncopeRound2.txt','w')
for exp in exponents:
	print str(exp) + '@No Syncope' 
	outfile.write(str(exp) + '@No Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] != 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')
	print str(exp) + '@Syncope' 
	outfile.write(str(exp) + '@Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] == 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')

outfile.close()

#Eliminate grammars without Syncope after Preterite and without Syncope after Durrative

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		cont = True
		if True in ['Preterite:' in x for x in item[1]]:
			index = ['Preterite:' in x for x in item[1]].index(True)
			if 'Syncope' not in item[1][index + 1]:
				cont = False
		if cont and (True in ['Durrative:' in x for x in item[1]]):
			index = ['Durrative:' in x for x in item[1]].index(True)
			if 'Syncope' not in item[1][index + 1]:
				cont = False
		if cont:
			try:
				newgrammars[key] += [item]
			except:
				newgrammars[key] = [item]


grammars = newgrammars

#Check for Syncope Consistancy with each item
outfile = open('ResultsForSyncopeRound3.txt','w')
for exp in exponents:
	print str(exp) + '@No Syncope' 
	outfile.write(str(exp) + '@No Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] != 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')
	print str(exp) + '@Syncope' 
	outfile.write(str(exp) + '@Syncope' + '\n')
	for key in grammars:
		if exp.split(':')[0] in key:
			numof = 0
			for item in grammars[key]:
				searchstring = [exp in x for x in item[1]]
				if True in searchstring:
					try:
						if item[1][searchstring.index(True)+1] == 'Syncope':
							numof += 1
					except:
						continue
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')

outfile.close()

#Test Orders
orders = [['G','D','S','N'],['','t1','t2','tn'],['Durrative','Preterite']]
combos = [(x1,x2) for y1 in orders for y2 in orders for x1 in y1 for x2 in y2 if (y1 != y2)]

outfile = open('ResultsForOrderings.txt','w')
for combo in combos:
	print str(combo)
	outfile.write(str(combo) + '\n')
	for key in grammars:
		if set(combo).issubset(set(key)):
			numof = 0
			for item in grammars[key]:
				cor_order = False
				cur_item = 0
				for el in item[1]:
					if combo[cur_item]+':' in el:
						if cur_item < 1:
							cur_item += 1
						else:
							cor_order = True
							break
					elif (cur_item == 0) and (combo[1]+':' in el):
						break
				if cor_order:
					numof += 1
			print '\t' + str(key) + ': ' + str(numof)
			outfile.write('\t' + str(key) + ': ' + str(numof) + '\n')

outfile.close()

#First round of elimination by infix amount

for key in possible_reflexes:
	for reflex in possible_reflexes[key]:
		print key + ':' + reflex
		highest_infix = 0
		for key2 in grammars:
			if key in key2:
				for item in grammars[key2]:
					if (key != 'cut') and (key + ':' + reflex + ',' in item):
						infixnum = item.split(key + ':' + reflex + ',')[1][:2]
						try:
							infixnum = int(infixnum)
						except:
							infixnum = int(infixnum[0])
						if infixnum > highest_infix:
							highest_infix = infixnum
					elif (key == 'cut'):
						continue
		print '\t' + str(highest_infix)

infixes = {
'D:an':9,
'D:n':9,
'D:na':6,
'N:na':4,
'S:sa':2,
't2:ta':4,
't2:t':4,
't1:ta':4,
't1:t':4,
'tn:tan':3,
'Durrative:an':9,
'Durrative:n':9}

outfile = open('ResultsForInfixesRound1.txt','w')
for key in infixes:
	for iamount in range(infixes[key]+1):
		print key + ',' + str(iamount)
		outfile.write(key + ',' + str(iamount) + '\n')
		for key2 in grammars:
			if key.split(':')[0] in key2:
				numof = 0
				for item in grammars[key2]:
					if (key != 'cut') and (key + ',' + str(iamount) in item):
						numof += 1
				print '\t' + str(key2) + ': ' + str(numof)
				outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

# Only keep infix amounts that can generate everything:
keepers = [
['D:na,2',
'D:n,2',
'D:an,1',
'D:an,2'],
['Durrative:an,2',
'Durrative:n,2'],
['t1:t,1',
't1:ta,1',
't1:ta,2'],
['t2:ta,1',
't2:ta,2',
't2:t,1'],
['S:sa,0'],
['tn:tan,2'],
['N:na,0']]

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		if False not in [True in [y in item for y in x]  for x in keepers if x[0].split(':')[0] + ':' in item]:
			try:
				newgrammars[key] += [item]
			except:
				newgrammars[key] = [item]

#Second round of elimination

keepers = [
'D:na,2',
'D:n,2',
'D:an,1',
'D:an,2',
'Durrative:an,2',
'Durrative:n,2',
't1:t,1',
't1:ta,1',
't1:ta,2',
't2:ta,1',
't2:ta,2',
't2:t,1',
'S:sa,0',
'tn:tan,2',
'N:na,0']

outfile = open('ResultsForInfixesRound2.txt','w')
for key in keepers:
	print key
	outfile.write(key + '\n')
	for key2 in newgrammars:
		if key.split(':')[0] in key2:
			numof = 0
			for item in newgrammars[key2]:
				if (key in item):
					numof += 1
			print '\t' + str(key2) + ': ' + str(numof)
			outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

# Only keep infix amounts that can generate everything (Eliminate Durrative:n,2):
keepers = [
['D:na,2',
'D:n,2',
'D:an,1',
'D:an,2'],
['Durrative:an,2'],
['t1:t,1',
't1:ta,1',
't1:ta,2'],
['t2:ta,1',
't2:ta,2',
't2:t,1'],
['S:sa,0'],
['tn:tan,2'],
['N:na,0']]

newgrammars = {}
for key in grammars:
	for item in grammars[key]:
		if False not in [True in [y in item for y in x]  for x in keepers if x[0].split(':')[0] + ':' in item]:
			try:
				newgrammars[key] += [item]
			except:
				newgrammars[key] = [item]

#Third round of elimination

keepers = [
'D:na,2',
'D:n,2',
'D:an,1',
'D:an,2',
'Durrative:an,2',
't1:t,1',
't1:ta,1',
't1:ta,2',
't2:ta,1',
't2:ta,2',
't2:t,1',
'S:sa,0',
'tn:tan,2',
'N:na,0']

outfile = open('ResultsForInfixesRound3.txt','w')
for key in keepers:
	print key
	outfile.write(key + '\n')
	for key2 in newgrammars:
		if key.split(':')[0] in key2:
			numof = 0
			for item in newgrammars[key2]:
				if (key in item):
					numof += 1
			print '\t' + str(key2) + ': ' + str(numof)
			outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()


# Permutation Elimination 1
D_pos = (
'D:na,2',
'D:n,2',
'D:an,1',
'D:an,2')
t1_pos = (
't1:t,1',
't1:ta,1',
't1:ta,2')
t2_pos = (
't2:ta,1',
't2:ta,2',
't2:t,1')
Durr_pos ='Durrative:an,2'
S_pos = 'S:sa,0'
tn_pos = 'tn:tan,2'
N_pos = 'N:na,0'

combos = combinations([D_pos,t1_pos,t2_pos],3)

comb_pos = [(x1,x2,x3) for x in combos for x1 in x[0] for x2 in x[1] for x3 in x[2]]

outfile = open('ResultsForCombsRound1.txt','w')
for pos in comb_pos:
	print pos
	outfile.write(str(pos) + '\n')
	for key2 in newgrammars:
		if True in [x.split(':')[0] in key2 for x in pos]:
			numof = 0
			for item in newgrammars[key2]:
				if False not in [x in item for x in pos if x.split(':')[0] + ':' in item]:
					numof += 1
			print '\t' + str(key2) + ': ' + str(numof)
			outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

#Eliminate Combinations - Failed All Variants Possible - Try 2
combos = [D_pos,Durr_pos,t1_pos,t2_pos]
fixed = [S_pos,N_pos,tn_pos]

comb_pos = [(x1,x2) for x in combos for x1 in fixed for x2 in x]

outfile = open('ResultsForCombsRound2.txt','w')
for pos in comb_pos:
	print pos
	outfile.write(str(pos) + '\n')
	for key2 in newgrammars:
		if True in [x.split(':')[0] in key2 for x in pos]:
			numof = 0
			for item in newgrammars[key2]:
				if False not in [x in item for x in pos if x.split(':')[0] + ':' in item]:
					numof += 1
			print '\t' + str(key2) + ': ' + str(numof)
			outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()

#No more easy eliminations, recheck grammar space
possible_reflexes = {
'cut':['parVs'],
'G':[''],
'N':['na'],
'D':['an','n','na'],
'S':['sa'],
't1':['ta','t'],
't2':['ta','t'],
'tn':['tan'],
'':[''],
'Preterite':[''],
'Durrative':['an'],
'3sg':['V']
}

#Retest afte eliminations
outfile = open('ResultsForReflexesAfterInfix.txt','w')
for key in possible_reflexes:
	for reflex in possible_reflexes[key]:
		print key + ':' + reflex
		outfile.write(key + ':' + reflex + '\n')
		for key2 in newgrammars:
			if key in key2:
				numof = 0
				for item in newgrammars[key2]:
					if (key != 'cut') and (key + ':' + reflex + ',' in item):
						numof += 1
					elif (key == 'cut') and (key + ':' + reflex in item):
						numof += 1
				print '\t' + str(key2) + ': ' + str(numof)
				outfile.write('\t' + str(key2) + ': ' + str(numof) + '\n')

outfile.close()


