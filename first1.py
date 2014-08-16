from bottle import route,request,run,template,post,get
import MySQLdb
import re
import feature_ext
import summary
ff=open("fopairs",'w')
@get('/admin')
def first():
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	query='select * from phones_db'
	try:
		cur.execute(query)
	except:
		return 'Database Error'
	rows=cur.fetchall()
	output=template('home',row=rows)
	db.close()
	return output
@get('/user')
def main():
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	query='select * from phones_db'
	try:
		cur.execute(query)
	except:
		return 'Database Error'
	rows=cur.fetchall()
	output=template('user_homepage',row=rows)
	db.close()
	return output
@post('/test')
def main():
	import feature_ext
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	review=request.forms.get('review')
	ff=open('sample.txt','w')
	feature_ext.feature(review,'sample',cur,ff)
	ff.close()
	ff=open('sample.txt','r')
	data=ff.read()
	ff.close()
	db.close()
	return data		
@post('/second')
def main():
	import ff_pruning
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	pname=request.forms.get('phone')
	pname=re.sub('-','_',pname)
	query='select * from '+pname
	try:
		cur.execute(query)
	except:
		db.close()
		return 'DataBase Error'
	if cur.rowcount==0:
		db.close()
		return 'No Reviews Found yet'
	rows=cur.fetchall()
	ff=open(pname+'_features','w')
	for r in rows:
		feature_list=feature_ext.feature(r[1],pname,cur,ff)
	ff.close()
	s_v=summary.summary(pname+'_features')
	s_v=ff_pruning.ff_pruning(s_v)
	db.close()
	return template('summary_display',s_v=s_v)
@post('/third')
def main():
	import re
	import cr_re_f
	import cr_re

	pname=request.forms.get('pname')
	option=request.forms.get('option')
	if pname.find('www')==-1:
		cr_re.cr_re(pname)
	else:
		cr_re_f.cr_re(pname)
		
	return 'Adding Reviews to Databse'


@post('/summary_display')
def main():
	import ff_pruning
	import re
	import summary
	pname=request.forms.get('phone')
	pname=re.sub('-','_',pname)
	s_v=summary.summary(pname+'_features')
	s_v=ff_pruning.ff_pruning(s_v)
	return template('summary_display',s_v=s_v)
run(host='0.0.0.0', port=8080)

	
