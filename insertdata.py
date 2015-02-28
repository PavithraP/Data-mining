import MySQLdb
from random import randint
db = MySQLdb.connect(host="localhost",user="root",
                	      passwd="hello123",db="data_mining") 
cur = db.cursor() 
points=[[0 for j in range(8)] for i in range(120)]
with open('./diagnosis.txt') as f:
        points = [[str(x) for x in line.rstrip('\r\n').split('	')] for line in f]
for i in range(120):
	try:
		print points[i]
		for j in range(1,8):
			if points[i][j] == "yes":
				points[i][j] = 1
			else:
				points[i][j] = 0
#		cur.execute("insert into node_info values(%d,%d,%d,%d,%d,%d,%d)" % (randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100)))
		#cur.execute("insert into table_site_info values(%d,'%s',%d,%d)" % (nodeId[randint(0,9)],table[randint(0,5)],0,0))
		cur.execute("insert into patient_info values(%f,%s,%s,%s,%s,%s,%s,%s)" % (float(points[i][0]),int(points[i][1]),int(points[i][2]),int(points[i][3]),int(points[i][4]),int(points[i][5]),int(points[i][6]),int(points[i][7])))
	#	cur.execute("insert into table_site_info values(%d,'%s')" % (nodeId[randint(0,18)],table[randint(0,5)]))

		db.commit()
	except Exception as e:
		print "Error",e

cur.close()
db.close()
