import MySQLdb
import re


db = MySQLdb.connect(host="localhost",user="root",passwd="hello123",db="data_mining")
cur = db.cursor() 
binaryAttributes=["nausea","lumbarPain","urinePushing","micturitionPains","urethraBurning","inflammationOfUB","nephritis"]
first=[]
length = len(binaryAttributes)
try:
	for i in range(length):
		for j in range(2):
			count = [0 for m in range(length)]
			cur.execute("SELECT count(*) FROM patient_info where %s = %d"%(binaryAttributes[i],j))
			noOfTuples = cur.fetchone()[0]
			cur.execute("SELECT * FROM patient_info where %s = %d"%(binaryAttributes[i],j))
			first = cur.fetchone()
			for row in cur.fetchall() :
				for k in range(1,8):
					if row[k] == first[k]:
						count[k-1] += 1
			cur.execute("insert into ifTable(ifAttribute,value) values('%s','%s')" % (binaryAttributes[i],first[i+1]))
			cur.execute("SELECT LAST_INSERT_ID()")
			lastId = cur.fetchone()[0]
			for k in range(length):
				if count[k] == (noOfTuples-1) and k != i :
					cur.execute("insert into thenTable values(%d,'%s','%s')" % (lastId,binaryAttributes[k],first[k+1]))
			db.commit()
	cur.execute("SELECT id,thenAttribute,value FROM thenTable order by id")
	thenIds = cur.fetchall()
	i=0
	noOfRules = 1	
	while(i < len(thenIds)):
		currentId = thenIds[i][0]
		cur.execute("SELECT ifAttribute,value FROM ifTable where id = %d"%(currentId))	
		ifId = cur.fetchone()
		print "Rule",noOfRules,"IF ",ifId[0],"=",ifId[1],
		print "THEN ",
		print thenIds[i][1],"=",thenIds[i][2],
		i+=1
		while(i < len(thenIds) and thenIds[i][0] == currentId):
			print ",",thenIds[i][1],"=",thenIds[i][2],
			i+=1
		print "\n"	
		noOfRules+=1		
				
except Exception as e:
	print "Error",e
cur.close()
db.close()
