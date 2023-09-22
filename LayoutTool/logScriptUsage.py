import maya.cmds as cmds
import os
import json
import sqlite3
from datetime import datetime

class LogScriptUsage:
	def __init__(self):

		with open(__file__.split('\\')[0] + '/data/settings.json', 'r') as f:
			settings = json.load(f)

		self.dbpath = settings["db_file"]
		self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.user = os.getenv('USERPROFILE').split('\\')[-1]
		self.filename = cmds.file(q = True, sn = True).split('/')[-1]

	def addScriptData(self, script, runfrom):
		con = sqlite3.connect(self.dbpath)
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

	def addUiData(self, command, subCommand):
		con = sqlite3.connect(self.dbpath)
		cursor = con.cursor()

		cursor.execute("""
			SELECT name FROM sqlite_master
			WHERE type='table'
			""")
		data = cursor.fetchall()

		# timestamp, user, script, run from
		if not data or 'ui_usage' not in [i[0] for i in data]:
			cursor.execute("""CREATE TABLE ui_usage
				("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				"timestamp" TIMESTAMP, "user" TEXT,
				"command" TEXT, "subCommand" TEXT, "filename" TEXT);""")

		# add data
		cursor.execute("""
			INSERT into ui_usage 
			(timestamp, user, command, subCommand, filename)
			VALUES (?, ?, ?, ?, ?);
			""", (self.timestamp, self.user, command, subCommand, self.filename))
		con.commit()

		cursor.close()
		con.close()