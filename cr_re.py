import re
import urllib2
import nltk
import MySQLdb
def acount(url):
	
	page=urllib2.urlopen(url).read()
	last=len(page)
	tbegin=page.find("productSummary")
	tpage=page[tbegin:last]
	tend=tpage.find("</div>")
	tpage=tpage[0:tend]
	tbegin=tpage.find("<b>")
	tend=tpage.find("</b>")
	tpage=tpage[tbegin:tend]
	tpage=nltk.clean_html(tpage)
	no=''.join(tpage)
	no=no.split(' ')
	no=no[0]
	no=re.sub(r'[^0-9]','',no)
	return int(no)

def areview(url,pname,cur):
	rcount=0
	try:
		page=urllib2.urlopen(url).read()
	except:
		print 'Returning from amazon proc'
		return rcount
	last=len(page)
	begin=page.find("id=\"productReviews")
	end=page.find("</table><br />")
	page=page[begin:end]

	rbegin=page.find("<div class=\"reviewText\">")
	
	while rbegin != -1:
		rcount=rcount+1
		page=page[rbegin:end]
		rend=page.find("</div>")
		review=page[0:rend]
		review=nltk.clean_html(review)
		query='insert into '+pname+'(reviews) values("'+review+'")'
		try:
			cur.execute(query)
			print 'Inserted'
		except:
			'Flipkart Review Could not Be Inserted'
		page=page[rend:end] 
		rbegin=page.find("<div class=\"reviewText\">")
	return rcount
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
def extract(review,pname,cur):
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
		'Flipkart Review Could not Be Inserted'
	
	return

def freview(url,pname,cur):
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

	rpage=urllib2.urlopen(url).read()
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
def cr_re(pnam):
	db=MySQLdb.connect('localhost','root','root','reviews1')
	cur=db.cursor()
	base_url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="
	a_flag=0
	f_flag=0
	f_r_data=''
	a_r_data=''
	acounts=1
	fcounts=1
	apcount=1
	fpcount=0

	pname=re.sub(' ','%20',pnam)
	print pname
	f_search=base_url+pname+'%20Reviews%20Flipkart'
	a_search=base_url+pname+'%20Reviews%20Amazon'

	try:
		f_result=urllib2.urlopen(f_search)
		a_result=urllib2.urlopen(a_search)
		f_r_data=f_result.read()
		a_r_data=a_result.read()
		f_r_data=str(f_r_data)
		a_r_data=str(a_r_data)
	except:
		print 'Connection Error'




	#URL extractor
	f_url=re.search(r"http://www.flipkart.com/[^/]*/product-reviews/[A-Z0-9]{16}",f_r_data)
	a_url=re.search(r'www.amazon.com/[a-zA-Z0-9_-]*/product-reviews/[A-Z0-9]{10}',a_r_data)

	#phone name and phone id and from where it has been choosen
	try:
		f_url=str(f_url.group())
		f_flag=1
		temp=f_url.split('/')
		pname=str(temp[3])
		f_id=temp[5]
		print f_url
	
	except: 
		print 'No Reviews from the Flipkart'
		f_id='-'
		f_url='-'
	try:
		a_url=str(a_url.group())
		a_flag=1
		temp=a_url.split('/')
		a_id=temp[3]
	
		if f_flag==0:
			f_url=raw_input()
			pname=str(temp[1])
			temp=f_url.split('/')
			pname=str(temp[3])
			f_id=temp[5]
			f_flag=1
	except:
		print 'No Reviews from the Amazon'			
		a_id='-'
		a_url='-'
	try:
		query='select * from phones_db where pname="'+pname+'"'
		cur.execute(query)
	except:
		print 'Database Error'
	if cur.rowcount==0:
		query='insert into phones_db(pname,fid,aid,furl,aurl) values("'+pname+'","'+f_id+'","'+a_id+'","'+f_url+'","'+a_url+'")'
		try:
			cur.execute(query)
		except:
			print 'Insertion of data in to phones_db failed'
	

	pname=pname.replace('-','_')
	if f_flag==1 or a_flag==1:
		query='create table '+pname+'(rid int not null auto_increment,reviews TEXT,primary key(rid))'
		try:
			cur.execute(query)
		except:
			print 'Table Could not be created'
	if a_flag==1:
		a_url='http://'+a_url
		a_r_count=acount(a_url)
		print a_r_count
		print a_url	
		while acounts < a_r_count:
			url=a_url+'/?pageNumber='+str(apcount)	
			acounts=acounts+areview(url,pname,cur)
			apcount=apcount+1
			db.commit()
			print acounts
	print pname
	if f_flag==1:
		f_r_count=fcount(f_url)
		print f_r_count
		print f_url
			
		while(fcounts<=f_r_count):
			url=f_url+"?&start="+str(fpcount)
			fcounts=fcounts+freview(url,pname,cur)
			fpcount=fpcount+10
			db.commit()
			print fcounts
	
	
	db.commit()
	db.close()

