#for each opinion word call the following function which returns +1 or -1

def opine_orientation(word,neg):
	from nltk.corpus import wordnet
	import MySQLdb
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	seed_list=[]
	syn_list=[]
	ant_list=[]
	word=word.lower()
	cur.execute('select value from seed_list where adj="'+word+'"')
	if cur.rowcount==0:
		cur.execute('select * from seed_list')
		rows=cur.fetchall()
	else:
		value=cur.fetchone()
		return int(value[0])
		
	syn_set=wordnet.synsets(word,'a')
	for s in syn_set:
		for l in s.lemmas:
			if l.name != word:
				syn_list.append(l.name)
			antonym=l.antonyms()
			if len(antonym)!=0:
				for a in antonym:
					ant_list.append(a.name)
						
	for s in syn_list:
		for r in rows:
			if r[0]==s:
				query='insert into seed_list(adj,value) values("'+word+'","'+str(r[1])+'")'
				print query
				try:
					print query
					cur.execute(query)
				except :
					print 'Database Errormn'
					print r[0] + s
					
				db.commit()
				if neg==1:
				   if r[1]==-1:
				      return 1
				   else:
				      return -1
				return r[1]
	for a in ant_list:
		for r in rows:
			if r[0]==a:
				query='insert into seed_list(adj,value) values("'+word+'",'+ str(r[1] * -1)+')'
				try:
					cur.execute(query)
				except :
					print 'Database Errorn'
		
				db.commit()
				if neg==1:
				   if r[1]==-1:
				      return 1
				   else:
				      return -1
				return r[1]
	return 'Not found'
		
