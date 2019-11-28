import sqlite3

class Connection:
	def make_connection(self):
		conn = sqlite3.connect('PlusHealth.db')
		
		return conn