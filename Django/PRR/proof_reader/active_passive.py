from pattern.en import parsetree, conjugate


a_to_p_prp = {'i':'me', 'you':'you', 'we':'us', 'they':'them', 'it':'it', 'he':'him', 'she':'her'}
temp = {}
for x,y in a_to_p_prp.items():
	temp[y] = x

a_to_p_prp.update(temp)

def active_passive(sent): # sent is a string 
	sent = sent.lower()
	pt = parsetree(sent, relations=True, lemmata=True)
	last_np = " by"
	first_np = ""
	verb_form = [0, 0] 
	vp = ""
	verb_sing=True
	# 1 past, 2-present, 3-future
	# 1-simple, 2-continuous, 3-perfect
	for sentence in pt:
		for chunk in sentence.chunks:
			 print(chunk.type, [(w.string, w.type) for w in chunk.words], type(chunk.words))

		if(sentence.chunks[0].type=='NP'):
			for w in sentence.chunks[0].words:
				try:
					last_np += " "+a_to_p_prp[w.string]
				except KeyError:
					last_np += " "+w.string

		if(sentence.chunks[1].type=='VP'):
			last_verb = sentence.chunks[1].words[-1]	
			w_list = [x.string for x in sentence.chunks[1].words]
			t_list = [x.type for x in sentence.chunks[1].words]
			if (last_verb.type=='VBD' or last_verb.type=='VBN' ):
				verb_form[0] = 1
			elif(last_verb.type=='VBP' or last_verb.type=='VBZ' or last_verb.type=='VB' or last_verb.type=='MD'):
				verb_form[0] = 2
				verb_form[1] = 1
			elif (last_verb.type=='VBC' or last_verb.type=='VBF'):
				verb_form[0] = 3
			elif (last_verb.type=='VBG'):
				verb_form[1] = 2
				if (('was' in w_list) or ('were' in w_list)): verb_form[0]=1
				else: verb_form[0]=2

			if(('has' in w_list) or ('have' in w_list)):
				verb_form[0]=2
				verb_form[1]=3

			if('had' in w_list):
				verb_form[0]=1
				verb_form[1]=3

			if (('will' in w_list) or ('shall' in w_list) or ('would' in w_list) or ('should' in w_list)):
				verb_form[0]=3

			if(('VBG' in t_list) and ('VB' in t_list)):
				vp += ' '.join(w_list[t_list.index('VBG') : t_list.index('VB')])+' be '
			vp += conjugate(last_verb.string, 'VBN')

		if(sentence.chunks[2].type=='NP'):
			noun_found = False
			for w in sentence.chunks[2].words:
				if noun_found:
					last_np += " "+w.string
				elif ('NN' in w.type) or ('PRP' in w.type):
					try:
						first_np += a_to_p_prp[w.string]+" "
					except KeyError:
						first_np += w.string+" "
					if 'S' in w.type:
						verb_sing = False

					if((verb_form[1]==3) and (verb_form[0]==2)):
						if(verb_sing):
							first_np+="has been "
						else:
							first_np+="have been "

					elif((verb_form[1]==3) and (verb_form[0]==1)):
						first_np+="had been "

					
					elif((verb_form[0]==2)):
						if(verb_sing):
							first_np+="is "
						else:
							first_np+="are "
						
						# elif(verb_form[1]==3):
					elif((verb_form[0]==1)):
						if(verb_sing):
							first_np+="was "
						else:
							first_np+="were "

					elif((verb_form[0]==3)):
						if(verb_sing):
							first_np+="will be "
						else:
							first_np+="would be "

					if(verb_form[1]==2):
							first_np+="being "


					noun_found=True
					
				else:
					first_np += w.string+" "

		if(len(sentence.chunks)>3):
			if(sentence.chunks[3].type=='ADVP'):
				w_list = [x.string for x in sentence.chunks[3].words]
				vp += ' '+' '.join(w_list)



	return first_np+vp+last_np