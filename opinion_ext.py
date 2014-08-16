#this function is called for every feature extracted to get its opinion word
import nltk
import orientation

def opinion(feature,sentence,pname,cur,ff):
	findex=0
	#preprocessing incase feature contains more than 1 word
	feature1=nltk.word_tokenize(feature)
	str1=nltk.word_tokenize(sentence)
	#ff.write(str(str1))
	#ff.write('\n')
	flen=len(feature1)
	
	if flen>1:
		str2=['\0']
		for s1 in str1:
		    str2.append(s1)
		slen=len(str2)
		
		i=1
		j=0
		tok=[]
		
		while(i<slen):    
		    if str2[i]==feature1[0]:
			tok.append(feature)
			i=i+flen
		    else:
			tok.append(str2[i])
			i=i+1
	else:
		tok=nltk.word_tokenize(sentence)
		
	adj=[]
	neg=0
	#find the index of the feature word
	i=0

	for s in tok:
	    if s==feature:
	       findex=i
	       break
	    if s=="not":
	       neg=1
	       ff.write("not")
	    i=i+1
	
	tstr=nltk.pos_tag(str1)
	#ff.write(str(tstr))
	#ff.write('\n')
	# find all the adjectives
	for (w,t) in tstr:
	    if t=="JJ" and feature.find(w)==-1:
	       adj.append(w)
	    elif t==("JJR" or "JJS"):
	       adj.append(w)
	    
	

	feat=[]
	length=len(adj)
	#if no adj is found then take the adj present in the noun phrase
	if length==0:
		ftok=nltk.word_tokenize(feature)
		ftag=nltk.pos_tag(ftok)
		for (w,t) in ftag:
			if t=="JJ":
			   adj.append(w)
			else:
			   feat.append(w)
		if len(adj)!=0:
			opinion=' '.join(adj)
			feature=' '.join(feat)
			orient=orientation.opine_orientation(opinion,neg)
			#print "selected "+feature
			if orient != "Not found":
				feop=feature+"/"+opinion+"/"+str(orient)
				ff.write(feop)
				ff.write('\n')			
				#query='insert into '+pname+'_f(feature) values("'+feature+'")'
			#orient=str(orient)
			#query='insert into '+pname+'_f(feature,orien) values("'+feature+'","'+orient+'")'
			#try:
				#cur.execute(query)
				#db.commit()
			#except:
				#print 'Could not Insert into Database1'
			#include the db stmnts for inserting the orientation for the feature
			#print feature+' '+orient
			return 0
		elif len(adj)==0:
			for (w,t) in tstr:
				if t==("VBN" or "VBJ" or "VBD" or "VBP" or "VBZ" or "VBG"):
	       				adj.append(w)
		   	if len(adj)==0:
				return -1

	else:
		dist={}
		i=0
	        j=0

		#calculate the distance of each adj from the feature
		for s in str1:
			if j>=length:
			  break
			if s==adj[j]:
			   j=j+1
			   if i>findex:
			      dist[s]=i-findex
			   else:
			      dist[s]=findex-i
			i=i+1

		d1=dist.values()
		min=d1[0]

		for n in d1:
		   if n<min:
		      min=n

		dist=dist.items()

		for key,val in dist:
		    if val==min:
		       opinion=key

		orient=orientation.opine_orientation(opinion,neg)
		#print "selected "+feature
		if orient != "Not found":
			feop=feature+"/"+opinion+"/"+str(orient)
			ff.write(feop)
			ff.write('\n')	
		#orient=str(orient)
		#query='insert into '+pname+'_f(feature) values("'+feature+'")'
		#query='insert into '+pname+'_f(feature,orien) values("'+feature+'","'+orient+'")'
		#try:
			#cur.execute(query)
			#db.commit()
		#except:
			#print 'Could not Insert into Database'
		return 0
