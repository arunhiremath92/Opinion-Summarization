def extract(review,pname,cur):
	import nltk
	ubegin=review.find("<a")
	if ubegin < 0:
	   ubegin=review.find("<span")
	   uend=review.find("</span")
	else:
	   uend=review.find("</a>")

	
	user=review[ubegin:uend]
	user=nltk.clean_html(user)
	#print "USER:"+user
	rend=review.find("Was this review helpful?")
	rbegin=ubegin
	review=review[rbegin:rend]
	rbegin=review.find("<div")
	review=review[rbegin:rend]

	dbegin=review.find("<div")
	dend=review.find("</div>")
	date=review[dbegin:dend]
	date=nltk.clean_html(date)
	#print "DATE:"+date

	cbegin=review.find("<strong")
	cend=review.find("</strong>")
	content=review[cbegin:cend]
	content=nltk.clean_html(content)

	cbegin=review.find("<p")
	cend=review.find("</p>")
	content1=review[cbegin:cend]
	content1=nltk.clean_html(content1)
	content=content+"."+content1
	#print "CONTENT:"+content
	query='insert into '+pname+'(reviews) values("'+content+'")'
	try:
		cur.execute(query)
		print 'Inserted'
	except:
		print 'Flipkart Review Could not Be Inserted'
	fd=open(pname,'a')
	fd.write(content)
	fd.close()
	return

def freview(url,pname,cur):
	import urllib2
	import nltk
	rpage=urllib2.urlopen(url).read()
	begin=rpage.find("review-list")
	end=rpage.find("review-footer")
	rpage=rpage[begin:end]
	rcount=0
	while(begin != -1):
	    	rbegin=rpage.find("review-id")
	    	rend=rpage.find("Was this review helpful?")
	     	review=rpage[rbegin:rend]

	     	temp=review.find("<a href")
	     	if (temp != -1):
			rbegin=review.find("</a>")
	     	review=review[rbegin:rend]
	     	rbegin=review.find("</div>")
	     	review=review[rbegin:rend]
	     	extract(review,pname,cur)
	     	rcount=rcount+1
	     	begin=rend
	     	rpage=rpage[begin:end]
	     	begin=rpage.find("review-id")
	     	rpage=rpage[begin:end]
	     	
	return rcount

def fcount(url):
	import urllib2
	import nltk
	import re
	rcount=0
	try:
		rpage=urllib2.urlopen(url).read()
	except:
		return rcount
	
	tbegin=rpage.find("user-rating")
	tend=rpage.find("review-list")
	temp=rpage[tbegin:tend]

	tbegin=temp.find(" Write a Review")
	tend=temp.find("review-list")
	temp=temp[tbegin:tend]

	tbegin=temp.find("of")
	tend=temp.find("review-list")
	temp=temp[tbegin:tend]

	tbegin=temp.find("of")
	tend=temp.find("review-list")
	temp=temp[tbegin:tend]

	tbegin=temp.find("<strong")
	tend=temp.find("</strong>")
	temp=temp[tbegin:tend]

	temp=nltk.clean_html(temp)
	rcount=temp
	rcount=re.sub(r'[^0-9]','',rcount)
	return int(rcount)
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
def cr_re(f_url):
	import re
	import MySQLdb
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	print 'Inside cr_re_f'
	if f_url.find('http://')==-1:
		f_url='http://'+f_url
	temp=f_url.split('/')
	p_name=str(temp[3])
	p_name=re.sub('-','_',p_name)
	print p_name
	
	print f_url
	try:
		query='create table '+p_name+'(rid int not null auto_increment,reviews TEXT,primary key(rid))'
		cur.execute(query)
	except:
		print 'Table Already Exists'
		print 'Deleting all the Contents'
		try:
			cur.execute('delete from '+p_name)
		except:
			print 'Could not Delete Table contents'
	f_r_count=fcount(f_url)
	print f_r_count
	fcounts=0
	fpcount=0
	while fcounts < f_r_count:
			url=f_url+"?&start="+str(fpcount)
			fcounts=fcounts+freview(url,p_name,cur)
			fpcount=fpcount+10
			print fcounts
			db.commit()
	db.close()
