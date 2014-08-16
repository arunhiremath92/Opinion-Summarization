def ff_pruning(summary):
	import MySQLdb
	ff_itms=summary.items()
	ff_list={}
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	query='select * from feature_list'
	try:
		cur.execute(query)
	except:
		print 'Database Error'
	result=cur.fetchall()
	for (f,l) in ff_itms:
		for r in result:
			if r[1]==f:
				if ff_list.has_key(r[0]):
					tmp=ff_list[r[0]]
					t1=tmp[0]+l[0]
					t2=tmp[1]+l[1]
				else:
				   ff_list[r[0]]=l
				

	return ff_list
	db.close()
	

