import maya.cmds as cmds
import os
import sqlite3
from datetime import datetime

class LogScriptUsage:
	def __init__(self):
		
		self.path = 'C:/' # <--- database path. same as "view_usage_stat.py | Model()"
		
		self.dbfile = 'layouttool_script_usage.db'
		self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.user = os.getenv('USERPROFILE').split('\\')[-1]
		self.filename = cmds.file(q = True, sn = True).split('/')[-1]

	def addData(self, script, runfrom):
		con = sqlite3.connect(self.path + '/' + self.dbfile)
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
			""", (self.timestamp, self.user, script, runfrom, self.filename))
		con.commit()

		cursor.close()
		con.close()