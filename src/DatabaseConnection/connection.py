import sqlite3

class Connection:
	def make_connection():
		conn = sqlite3.connect('DatabaseConnection/PlusHealth.db')

		return conn