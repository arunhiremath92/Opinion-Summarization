query='create table 'pname+'_ff(feature varchar(15),pos int,neg int)'
	try:
		cur.execute(query)
	except:
		print pname+'_ff could not be created'
ff_file=open('try.txt','r')
	ff_set=ff_file.read()
	fd=open('fopairs','r')
	ff=fd.read()
	ff=ff.split('\n')
	for f in ff:
		temp=f.split('/')
		if len(temp[0])>1:
			if ff_set.find(temp[0]) == -1
				print 'Feature not included'
			#insert in to dbms
			else:
				query='select * from'+pname+'_ff where feature="'+temp[0]+'"'
				try:
					cur.execute(query)
				except:
					print 'something with summarizaton part'
				if cur.rowcount==0:
					query='insert into '+pname+'_ff(feature,pos,neg) values('
					if temp[1]==1
						db_query=query+temp[0]+'",'+str(temp[1])+str(0)
