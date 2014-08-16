import re
import summary
import feature_ext
import MySQLdb
db=MySQLdb.connect('localhost','root','root','reviews1')
cur=db.cursor()
#include the db statements to get the reviews

query='select * from phones_db'
try:
	cur.execute(query)
except:
	print 'Could not get the table details'
if cur.rowcount==0:
	print 'No phones in the database'
	
phones=cur.fetchall()
for p in phones:
	print str(p[0])+' '+p[1]
	pname=p[1]
	pname=re.sub('-','_',pname)
	print pname
	ff=open(pname+'_features','w')
	#query='create table '+pname+'_f(feature varchar(15),orien int)'
	#try:
		#print query
		#cur.execute(query)
		#print 'Table Created'
	#except:
		#print 'could not create feature table'
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
			feature_ext.feature(r[1],pname,cur,ff)
	
	ff.close()

for p in phones:
	pname=p[1]
	pname=re.sub('-','_',pname)
	summary.summary(pname+'_features')					
