import MySQLdb
db=MySQLdb.connect('localhost','root','root','reviews1')
fd=open('try3','r')
temp=fd.read()
temp=temp.split(',')
feature=raw_input()
feature=str(feature)
cur=db.cursor()
for t in temp:
	query='insert into feature_list(feature,fnames) values("'+feature+'","'+str(t)+'")'
	try:
		print query
		cur.execute(query)
		db.commit()
	except:
		print 'error'
db.commit()
db.close()
