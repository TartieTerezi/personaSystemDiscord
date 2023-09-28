import sqlite3

class Dao(object):
	"""docstring for DAO"""

	@classmethod
	def getOneDataBdd(cls,requete : str, argument : list):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute(requete,(argument))

		return res.fetchone()

	@classmethod
	def getCount(cls, requete : str, arguments : list) -> int:
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute(requete,(arguments))

		return int(res.fetchone()[0])

	@classmethod
	def getAll(cls,requete : str,arguments : list = []):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute(requete,arguments)
		return res

	@classmethod
	def insert(cls,requete : str, arguments : list):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute(requete,arguments)

		con.commit()
		cur.close()