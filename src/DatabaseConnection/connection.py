import sqlite3

#Class that allows us to connect to our sqlite database
class Connection:
	def make_connection():
		conn = sqlite3.connect('DatabaseConnection/PlusHealth.db')

		return conn