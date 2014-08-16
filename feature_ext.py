import preproc
import opinion_ext
import re

def gi_eq(w1,cur):
	w1=w1.upper()
	query1='select * from gi where words = "'+ w1+'"'
	query2='select * from gi where words REGEXP '+"'"+ w1+'#[2-9]'+"'"
	try:
		cur.execute(query1)
		if(cur.rowcount==0):
			cur.execute(query1)
			if cur.rowcount==0:
				return 1
	except:
		print 'database error'
	return 0

def pattern_match(p1):
	p=[('NN'),('NNP'),('NNS'),('NN NN'),('NN NN NN'),('JJ NN'),'(JJ NN NN)']
	for s1 in p:
		if p1 == s1:
			return p.index(s1)
	return 100

def chk_adj(w1,cur):
	w0=w1.split(' ');
	r_word=w0.pop(0)

	
	query='select * from adj where words="'+r_word+'"'
	try:
		cur.execute(query)
		if cur.rowcount==0:
			return w1
		else:
			return ' '.join(w0)
	except:
		print 'database error'


def feature(review,pname,cur,ff):
	import nltk
	from nltk.corpus import wordnet

	p0=[]
	w0=[]
	tags=[]
	words=[]
	p1=''
	f=[]
	stemmer=nltk.PorterStemmer()
	p=[('NN'),('NNP'),('NNS'),('NN NN'),('NN NN NN'),('JJ NN'),'(JJ NN NN)','(JJ JJ NN)']
	
	sentence=preproc.sentproc(review) #converts the review extracted into set of sentences

	for s in sentence:
		opine=0
		twords=nltk.word_tokenize(s)
		ttags=nltk.pos_tag(twords)
		for (w,t) in ttags:
			tags.append(t)
			words_stem=stemmer.stem(w)
			if len(wordnet.synsets(words_stem))== 0:
				words.append(w)
			else:
				words.append(words_stem)
		length=len(words)
		tempt=[length]
		tempw=[length]
		for k in range(0,length):
			tempt.append(tags[k])
			tempw.append(words[k])
			length=len(tempw)
			found=0
		for i in range(1,length-1):
			       	
			if(i<=length-4):
				x=4
			elif(i<=length-3):
				x=3
			elif(i<=length-2):
				x=2
			else:
				x=1
			j=x	
			while(j>0):	
				for t in range(i,i+j):
					p0.append(tempt[t])
					w0.append(tempw[t])
				p1=' '.join(p0)
				w1=' '.join(w0)
						
				p_m=pattern_match(p1)
				if p_m != 100:
					if gi_eq(w1,cur)==1: 
						i=i+j
						if p_m>4:
							w1=chk_adj(w1,cur)			
						f.append(str(w1))
						found=1
						break
				p0=[]
				w0=[]
				p1=''
				w1=''	
				j=j-1
				if found==1:
				   break
		
		for fp in f:
			op=opinion_ext.opinion(str(fp),s,pname,cur,ff)
			if op==-1:
			  	temp="dropped feature-"+fp
				#ff.write(temp)
				#ff.write('\n')
		f=[]
		tags=[]
		words=[]
