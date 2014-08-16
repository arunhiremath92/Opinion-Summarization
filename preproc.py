import re
import nltk
#takes review as a parameter and returns the set of sentences
def sentproc(review):
	final=[]

	if review.find('pro')!=-1:
		if review.find('*')!=-1:
			sent=review.split('*')
		elif review.find('-')!=-1:
			sent=review.split('-')
		else:
			sent=review
		for s in sent:
			if s.find('.')!=-1:
				temp=s.split('.')
			else:
				temp=s
			for t in temp:
				final.append(t)

	else:
		if review.find('.')!=-1:
			sent=review.split('.')
		else:
			sent=review.split('\n')
		for s in sent:
			if s.find(',')!=-1:
				temp=s.split(',')
				for t in temp:
					final.append(t)
			elif s.find(';')!=-1:
				temp=s.split(';')
				for t in temp:
					final.append(t)
			else:
				final.append(s)
	
	final1=[]
	final2=[]
	for f in final:
		f=re.sub('[pP][rR][oO][sS].','',f,re.I)
		f=re.sub('[cC][oO][nN][sS].','',f,re.I)
		f=re.sub('[^a-zA-Z0-9 ]*','',f)
		s=s.replace("'s",'s')
		final1.append(f)
	
	#processing in case of and
	for f in final1:
		tokf=nltk.word_tokenize(f)
		tagf=nltk.pos_tag(tokf)
		tags=[]
		words=[]
		temp=[]
		index=0
		flag=0
		k=0

		for (w,t) in tagf:
			tags.append(t)
			words.append(w)
		length=len(words)
		for t in tags:
			if t=="CC":
			   index=k
			   if index>1 and index<length-1:
				   if not((tags[index-1]=="NN") and (tags[index+1]=="NN")):
					   for t in range(0,index):
						temp.append(words[t])
					   final2.append(' '.join(temp))
					   temp=[]
					   for t in range(index+1,length):
						temp.append(words[t])
					   final2.append(' '.join(temp))
					   flag=1
					   break
			k=k+1
		if flag==0:
		    final2.append(f)
				
	return final2
	
