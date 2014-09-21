import MySQLdb as mdb
import sys, traceback
import time
from threading import Lock
import logging
import re

logger = logging.getLogger(__name__)

class DBCon(object):
	host = 'localhost'
	db = 'restauranttonight'
	user = 'root'
	passwd = ''
	port = 3306
	_instance = None
	con = None
	lock = Lock()

	def __init__(self, connection_string):
		pattrn = 'mysql://(.*)@(.*)/(.*)\?'
		tuple = re.compile(pattrn).findall(connection_string)[0]
		user_pass = tuple[0].split(':')
		if len(user_pass) == 2:
			self.user = user_pass[0]
			self.passwd = user_pass[1]
		else:
			self.user = user_pass[0]
			self.passwd = ''

		host_port = tuple[1].split(':')
		if len(host_port) == 2:
			self.host = host_port[0]
			self.port = int(host_port[1])
		else:
			self.host = host_port[0]

		self.db = tuple[2]
		try:
			self.con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
		except:
			logger.error(traceback.format_exc())


	def insert(self, query, tuple = None):
		con = self.con
		res = None
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
			#cursor = con.cursor(mdb.cursors.DictCursor)
			cursor = con.cursor()
			if tuple:
				cursor.execute(query, tuple)
			else:
				cursor.execute(query)
			res = cursor.lastrowid
			con.commit()
			
		except:
			#traceback.print_exc()
			logger.error(traceback.format_exc())
		
		return res

	def update(self, query, tuple = None):
		con = self.con
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
			cursor = con.cursor()
			if tuple:
				cursor.execute(query, tuple)
			else:
				cursor.execute(query)
			con.commit()
			return True
		except:
			logger.error(traceback.format_exc())
			return False
		


	def delete(self, query, tuple = None):
		return self.update(query, tuple)

	def fetch_one(self, query, tuple = None, tz = None):
		con = self.con
		res = None
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
			cursor = con.cursor(mdb.cursors.DictCursor)
			if tz:
				cursor.execute('set time_zone="' + tz + '"')
			if tuple:
				cursor.execute(query, tuple)
			else:
				cursor.execute(query)
			res = cursor.fetchone()
		except:
			logger.error(traceback.format_exc())
		
		return res



	def fetch_all(self, query, tuple = None):
		con = self.con
		res = []
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
			cursor = con.cursor(mdb.cursors.DictCursor)
			if tuple:
				cursor.execute(query, tuple)
			else:
				cursor.execute(query)
			res = cursor.fetchall()
		except:
			logger.error(traceback.format_exc())
		
		return res
	
	def updateAndGetStatus(self, query, tuple = None):		
		con = self.con
		noOfRowsAffected = 0
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
			cursor = con.cursor()
			if tuple:
				noOfRowsAffected = cursor.execute(query, tuple)
			else:
				noOfRowsAffected = cursor.execute(query)
			con.commit()
			if noOfRowsAffected > 0:
				return True
			else :
				return False
		except:
			logger.error(traceback.format_exc())
			return False
		
				
				
	def getDbConnectionInstance(self):
		con = self.con
		try:
			if con is None:
				con = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
		except:
			logger.error(traceback.format_exc())
		return con

	def __exit__(self):
		con = self.con
		try:
			if con:
				con.close()
		except:
			logger.error(traceback.format_exc())
		
