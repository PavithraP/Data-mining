import MySQLdb
import re

db = MySQLdb.connect(host="localhost",user="root",passwd="hello123",db="data_mining")
cur = db.cursor() 
binaryAttributes=["nausea","lumbarPain","urinePushing","micturitionPains","urethraBurning","inflammationOfUB","nephritis"]
first=[]
length = len(binaryAttributes)
try:
	cur.execute("delete from thenTableGAJA2")
	cur.execute("delete from ifTableGAJA2")
	cur.execute("delete from thenTable")
	cur.execute("delete from ifTable")
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
			cur.execute("insert into ifTableGAJA2 values(%d,'%s','%s')" % (lastId,binaryAttributes[i],first[i+1]))
			for k in range(length):
				if count[k] == (noOfTuples-1) and k != i :
					cur.execute("insert into thenTable values(%d,'%s','%s')" % (lastId,binaryAttributes[k],first[k+1]))
					cur.execute("insert into thenTableGAJA2 values(%d,'%s','%s')" % (lastId,binaryAttributes[k],first[k+1]))
			db.commit()
	attribInput = raw_input("Enter the attributes of interest\n")
	attribOfInterest=""
	for attribute in attribInput.split(","):
		attribOfInterest = attribOfInterest + "'" + attribute +"',"
	attribOfInterest = attribOfInterest[:-1]
	cur.execute("SELECT * FROM thenTableGAJA2 where thenAttribute in (%s) order by id"%(attribOfInterest))
	attribInThen = cur.fetchall()
	for attrib in attribInThen:
		print attrib[0],attrib[1],attrib[2]
		cur.execute("SELECT id FROM ifTableGAJA2 where ifAttribute = '%s' and value = '%s'"%(attrib[1],attrib[2]))
		ifId = cur.fetchone()
		cur.execute("SELECT ifAttribute,value FROM ifTableGAJA2 where id = %d"%(attrib[0]))
		attribInIf = cur.fetchall()
		for attribIf in attribInIf:
			cur.execute("insert into thenTableGAJA2 values(%d,'%s','%s')" % (ifId[0],attribIf[0],attribIf[1]))
			cur.execute("update thenTableGAJA2 set id = %d where id =%d" %(ifId[0],attrib[0]))
			cur.execute("delete from thenTableGAJA2 where id = %d and thenAttribute='%s'"%(ifId[0],attrib[1]))
	
	cur.execute("select id from ifTable where ifAttribute not in (%s)"%(attribOfInterest))
	notAttribOfInterest = cur.fetchall()
	for attrib in notAttribOfInterest:
		cur.execute("delete from thenTableGAJA2 where id = %d"%(attrib[0]))
	db.commit()
		
	#################Generating rule
	
	cur.execute("SELECT DISTINCT id,thenAttribute,value FROM thenTableGAJA2 order by id")
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
