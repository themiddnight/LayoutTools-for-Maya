import maya.cmds as cmds
import os
import sqlite3
import csv
from datetime import datetime

path = 'C:/'
dbfile = 'layouttool_script_usage.db'
csvfile = 'layouttool_script_usage.csv'

def getData():
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	user = os.getenv('USERPROFILE').split('\\')[-1]
	#userNum = str(sum([ord(i) for i in user]))
	filename = cmds.file(q = True, sn = True).split('/')[-1]
	return timestamp, user, filename

def addData(script, runfrom):
	timestamp, user, filename = getData()
	con = sqlite3.connect(path + dbfile)
	cursor = con.cursor()

	cursor.execute("""
		SELECT name FROM sqlite_master
		WHERE type='table'
		""")
	data = cursor.fetchall()

	# timestamp, user, script, run from
	if not data or 'script_usage' not in [i[0] for i in data]:
		cursor.execute("""CREATE TABLE script_usage
			("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			"timestamp" TIMESTAMP, "user" TEXT,
			"script" TEXT, "runfrom" TEXT, "filename" TEXT);""")

	# add data
	cursor.execute("""
		INSERT into script_usage 
		(timestamp, user, script, runfrom, filename)
		VALUES (?, ?, ?, ?, ?);
		""", (timestamp, user, script, runfrom, filename))
	con.commit()

	cursor.close()
	con.close()

def exportCsv():
	con = sqlite3.connect(path + dbfile)
	cursor = con.cursor()

	cursor.execute("""SELECT * FROM script_usage;""")
	data = cursor.fetchall()

	with open(path + csvfile, 'wb')as f:
		csv_writer = csv.writer(f)
		column_names = [description[0] for description in cursor.description]
		csv_writer.writerow(column_names)
		csv_writer.writerows(data)

	cursor.close()
	con.close()


#addData(user, filename, script, runfrom)
#exportCsv()