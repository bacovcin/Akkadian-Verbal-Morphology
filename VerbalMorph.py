from itertools import *
from sets import *

correct_forms = {
frozenset(('cut','G','','Preterite','3sg')):'VprVs',
frozenset(('cut','G','','Durrative','3sg')):'VparrVs',
frozenset(('cut','G','t1','Preterite','3sg')):'VptarVs',
frozenset(('cut','G','t1','Durrative','3sg')):'VptarrVs',
frozenset(('cut','G','tn','Preterite','3sg')):'VptarrVs',
frozenset(('cut','G','tn','Durrative','3sg')):'VptanarrVs',
frozenset(('cut','N','','Preterite','3sg')):'VpparVs',
frozenset(('cut','N','','Durrative','3sg')):'VpparrVs',
frozenset(('cut','N','tn','Preterite','3sg')):'VttaprVs',
frozenset(('cut','N','tn','Durrative','3sg')):'VttanaprVs',
frozenset(('cut','D','','Preterite','3sg')):'VparrVs',
frozenset(('cut','D','','Durrative','3sg')):'VparrVs',
frozenset(('cut','D','t1','Preterite','3sg')):'VptarrVs',
frozenset(('cut','D','t1','Durrative','3sg')):'VptarrVs',
frozenset(('cut','D','t2','Preterite','3sg')):'VptarrVs',
frozenset(('cut','D','t2','Durrative','3sg')):'VptarrVs',
frozenset(('cut','D','tn','Preterite','3sg')):'VptarrVs',
frozenset(('cut','D','tn','Durrative','3sg')):'VptanarrVs',
frozenset(('cut','S','','Preterite','3sg')):'VstaprVs',
frozenset(('cut','S','','Durrative','3sg')):'VstaprVs',
frozenset(('cut','S','t1','Preterite','3sg')):'VstaprVs',
frozenset(('cut','S','t1','Durrative','3sg')):'UstaparrVs',
frozenset(('cut','S','t2','Preterite','3sg')):'VstaprVs',
frozenset(('cut','S','t2','Durrative','3sg')):'VstaprVs',
frozenset(('cut','S','tn','Preterite','3sg')):'VstaprVs',
frozenset(('cut','S','tn','Durrative','3sg')):'VstanaprVs'
}
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

def Nassim(form):
	vowels = ['a','e','i','u','V']
	for i in range(len(form)):
		try:
			if (form[i] == 'n') and (form[i+1] not in vowels):
				form = form[:i] + form[i+1] + form[i+1:]
		except:
			continue
	return form

def Syncope(form):
	vowels = ['a','e','i','u','V']
	for i in range(len(form)):
		try:
			if (form[i] not in vowels) and (form[i+1] not in vowels) and (i+2 >= len(form)):
				form = Syncope(form[:i]+form[i+1:])
				break
			elif (form[i] not in vowels) and (form[i-1] in vowels) and (form[i+1] in vowels) and (form[i+2] not in vowels) and (form[i+3] in vowels):
				form = Syncope(form[:i+1]+form[i+2:])
				break
			elif (form[i] in vowels) and (form[i+1] in vowels):
				form = Syncope(form[:i+1]+form[i+2:])
				break
			elif (form[i] not in vowels) and (form[i+1] not in vowels) and (form[i+2] not in vowels):
				form = Syncope(form[:i]+form[i+1:])
				break
		except:
			continue
	return form

def Infix(form,infix,distance):
	return form[:distance] + infix + form[distance:]

def TryOrder(CurForm,RemainingItems,PastItems,CorForm):
	forms = []
	if CurForm == '':
		next_object = RemainingItems[0]
		for item in possible_reflexes[next_object]:
			if item == '':
				forms += TryOrder(item,RemainingItems[1:],PastItems+[next_object+':'+item],CorForm)
			else:
				forms += TryOrder(item,RemainingItems[1:],PastItems+[next_object+':'+item],CorForm)
				forms += TryOrder(Nassim(item),RemainingItems[1:],PastItems+[next_object+':'+item,'Nassim'],CorForm)
				forms += TryOrder(Syncope(item),RemainingItems[1:],PastItems+[next_object+':'+item,'Syncope'],CorForm)
				forms += TryOrder(Syncope(Nassim(item)),RemainingItems[1:],PastItems+[next_object+':'+item,'Nassim','Syncope'],CorForm)
				forms += TryOrder(Nassim(Syncope(item)),RemainingItems[1:],PastItems+[next_object+':'+item,'Syncope','Nassim'],CorForm)
	else:
		next_object = RemainingItems[0]
		for item in possible_reflexes[next_object]:
			if item == '':
				if len(RemainingItems) > 1:
					forms += TryOrder(Infix(CurForm,item,0),RemainingItems[1:],PastItems+[next_object+':Null'],CorForm)
				else:
					forms += [(Infix(CurForm,item,i),PastItems+[next_object+':Null'])]

			else:
				for i in range(len(CurForm)+1):
					if len(RemainingItems) > 1:
						forms += TryOrder(Infix(CurForm,item,i),RemainingItems[1:],PastItems+[next_object+':'+item+','+str(i)],CorForm)
						forms += TryOrder(Nassim(Infix(CurForm,item,i)),RemainingItems[1:],PastItems+[next_object+':'+item+','+str(i),'Nassim'],CorForm)
						forms += TryOrder(Syncope(Infix(CurForm,item,i)),RemainingItems[1:],PastItems+[next_object+':'+item+','+str(i),'Syncope'],CorForm)
						forms += TryOrder(Syncope(Nassim(Infix(CurForm,item,i))),RemainingItems[1:],PastItems+[next_object+':'+item+','+str(i),'Nassim','Syncope'],CorForm)
						forms += TryOrder(Nassim(Syncope(Infix(CurForm,item,i))),RemainingItems[1:],PastItems+[next_object+':'+item+','+str(i),'Syncope','Nassim'],CorForm)
					else:
						if Infix(CurForm,item,i) == CorForm:
							forms += [(Infix(CurForm,item,i),PastItems+[next_object+':'+item+','+str(i)])]
						if Nassim(Infix(CurForm,item,i)) == CorForm:
							forms += [(Nassim(Infix(CurForm,item,i)),PastItems+[next_object+':'+item+','+str(i),'Nassim'])]
						if Syncope(Infix(CurForm,item,i)) == CorForm:
							forms += [(Syncope(Infix(CurForm,item,i)),PastItems+[next_object+':'+item+','+str(i),'Syncope'])]
						if Syncope(Nassim(Infix(CurForm,item,i))) == CorForm:
							forms += [(Syncope(Nassim(Infix(CurForm,item,i))),PastItems+[next_object+':'+item+','+str(i),'Nassim','Syncope'])]
						if Nassim(Syncope(Infix(CurForm,item,i))) == CorForm:
							forms += [(Nassim(Syncope(Infix(CurForm,item,i))),PastItems+[next_object+':'+item+','+str(i),'Syncope','Nassim'])]
	return forms


def TestGrammars():
	decision_order=[('G','N','D','S'),('','t1','t2','tn'),('Preterite','Durrative')]
	possible_orders=[('cut',y,z,q,'3sg') for x in permutations(decision_order) for y in x[0] for z in x[1] for q in x[2]]
	possible_grammars={}
	for order in possible_orders:
		if frozenset(order) in correct_forms.keys():
			results = TryOrder('',order,[],correct_forms[frozenset(order)])
			for result in results:
				try:
					possible_grammars[frozenset(order)].append(result)
				except:
					possible_grammars[forzenset(order)] = [result]
	
#	outfile=open('Possible_Grammars.txt','w')
#	for result in results:
#		outfile.write(str(result)+'\n')
#	outfile.close()
			
TestGrammars()
