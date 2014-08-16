def summary(fname):
	print fname
	fd1=open(fname,'r')
	fd2=open(fname+'positive.txt','w')
	fd3=open(fname+'negative.txt','w')
	fd4=open('try.txt','r')
	fdc=open('companies.txt','r')
	cl=fdc.read()
	
	ff_list=fd4.read()
	contents=fd1.read()
	ff={}
	contents=contents.split('\n')

	for c in contents:
	
		temp=c.split('/')
		print c
		f=temp[0].lower()
		print temp
	
		if len(temp)!=0 and f!='':
			if ff_list.find(f)!=-1:
				if temp[2]== '1':
					fd2.write(f)
					fd2.write('\n')
				else:
					fd3.write(f)
					fd3.write('\n')	

	fd2.close()
	fd3.close()
	fd2=open(fname+'positive.txt','r+')
	fd3=open(fname+'negative.txt','r+')
	positive=fd2.read()
	negative=fd3.read()
	p_f={}
	n_f={}
	pve=[]
	nve=[]
	positive=positive.split('\n')
	negative=negative.split('\n')
	for p in positive:
		temp=p.lower()

		if p_f.has_key(temp):
			count=p_f[temp]
			count=count+1
			p_f[temp]=count
		else:
			p_f[temp]=1
			pve.append(p)
	print p_f
	for n in negative:
		temp=n.lower()
		if n_f.has_key(temp):
			count=n_f[temp]
			count=count+1
			n_f[temp]=count
		else:
			nve.append(n)
			n_f[temp]=1
	print n_f
	summary={}
	for p in pve:
		for n in nve:
			p=p.lower()
			n=n.lower()
			if p==n:
				if p_f[p]>1 or n_f[p]>1:
					print p +' POSITIVE '+ str(p_f[p]) + ' NEGATIVE '+ str (n_f[p])
					summary[p]=[p_f[p],n_f[p]]
		
	fd2.close()
	fd3.close()
	fd1.close()
	fd4.close()	
	return summary
	
