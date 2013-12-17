import _mysql
import sys
def dbconnect():
	try:
		con = _mysql.connect('127.0.0.1', 'root', '', 'tweets')
		con.query("SELECT VERSION()")
		result = con.use_result()
		print "Database connection succesfull"
		print "MySQL Database version: %s" % \
		result.fetch_row()[0]
		return con
	except _mysql.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)