import re
import nltk
import MySQLdb
from nltk.corpus import wordnet
stemmer=nltk.PorterStemmer()
db=MySQLdb.connect('localhost','root','root','reviews1')
cur=db.cursor()
fd=open('temp.txt','r')
fdr=open('try.txt','w')
sample=fd.read()
query='select * from phones_db'
try:
	cur.execute(query)
except:
	print 'Could not get the table details'
if cur.rowcount==0:
	print 'No phones in the database'
query='create table ff(feature varchar(20) not null)'
try:
	cur.execute(query)
	print 'Table Created'
except:
	print 'Table Already created'

	
phones=cur.fetchall()
for p in phones:

	pname=p[1]
	pname=re.sub('-','_',pname)
	print pname
	query='select * from '+pname
	try:
		cur.execute(query)		
	except:
		print 'review table error'
	
	if cur.rowcount==0:
		print 'No reviews Found'
	else:	
		rows=cur.fetchall()
		for r in rows:
			sample=r[1]
			sample=re.sub(r'[:;]',' ',sample)
			sentences=sample.split('.')
			ff={}
			count=0

			for s in sentences:
				words=nltk.word_tokenize(s);
				tag_words=nltk.pos_tag(words)
				for (w,t) in tag_words:
					if t=='NN' or t=='NNS' or t=='NNP':
						count=0
						w=w.lower()
						words_stem=stemmer.stem(w)
						c=len(wordnet.synsets(words_stem))
						if c== 0:
							w=w
						else:
							w=words_stem
						query='select * from gi where words="'+w+'"'
						try:
							cur.execute(query)
						except:
							print 'Something went wrong'
						if cur.rowcount==0:
							if ff.has_key(w):
								count=ff.get(w)
					
								count=count+1
								ff[w]=count
							else:
								ff[w]=1
			query='insert into ff(feature) values("'					
			features=ff.items()
			for (f,t) in features:
				if t>5:
					f=f.lower()
					fdr.write(f)
					fdr.write('\n')
					db_query=query+f+'")'
					try:
						cur.execute(db_query)
						db.commit()
					except:
						print f+' ->'+str(t)

db.close()
fdr.close()
fd.close()		
		
			

