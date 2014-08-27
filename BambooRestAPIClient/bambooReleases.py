#!/usr/bin/python

from __future__ import print_function
import sys
import datetime

try:
	import psycopg2
except ImportError:
	print("ImportError: This script needs psycopg2 module to work!")
	sys.exit(1)

class BambooReleases(object):
	""" class used for connecting to Bamboo DB """
	def __init__(self, db, dbhost, user, passwd):
		""" Takes db hostname, db name, user credentials for connecting to db """
		self.db     = db
		self.dbhost = dbhost
		self.user   = user
		self.passwd = passwd

	def dbConnect(self):
		""" Tries to connect to db and returns a connection if successful """
		try:
			conn_str = """dbname='{db}' user='{user}' host='{dbhost}'
			              password='{passwd}'""".format(db=self.db, user=self.user,
			              	                            dbhost=self.dbhost, passwd =self.passwd)
			conn  = psycopg2.connect(conn_str)
			return conn
		except: 
			print("ConnectionError: unable to connect to database")
			sys.exit(1)

	def queryDB(self, cur):
		""" Queries db for today releases in envname environment """
		now = datetime.datetime.now().strftime("%Y-%m-%d")
                print(now)
		query = """ SELECT dp.name AS deploy_name FROM deployment_project dp, deployment_environment de,
		            deployment_result dr WHERE dp.deployment_project_id = de.package_definition_id AND 
		            de.environment_id = dr.environment_id AND upper(de.name)='<environment>' AND
		            dr.finished_date>='{start_time}' AND dr.finished_date <='{end_time}' AND
		            upper(dr.deployment_state)='SUCCESSFUL' 
		            """.format(start_time = now +" 00:00:00", end_time = now + " 23:59:59")
		data = cur.execute(query)
                rows = cur.fetchall()
                return rows

if __name__ == '__main__':
	bRel = BambooReleases("<dbname>", "<db hostname>","<username>","<password>")
	conn = bRel.dbConnect()
	cur  = conn.cursor()
	rel_projects = bRel.queryDB(cur)
	#closing cursor and connection.
	cur.close()
	conn.close()
	projects = []
    for et in rel_projects:
        projects.append(et[0])
    print projects

