import MySQLdb
import re
db=MySQLdb.connect('localhost','root','root','reviews1')
cur=db.cursor()
query='select * from phones_db'
try:
	cur.execute(query)
except:
	print 'Could not get the table details'
ff=open('temp.txt','w')
phones=cur.fetchall()
for p in phones:
	pname=p[1]
	pname=re.sub('-','_',pname)
	query='select * from '+pname
	print query
	try:
		cur.execute(query)
	except:
		print 'Could not'
	rows=cur.fetchall()
	for r in rows:
		ff.write(str(r[1]))
db.close()
ff.close()
