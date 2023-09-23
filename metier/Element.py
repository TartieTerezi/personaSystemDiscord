import sqlite3

class Element(object):
	"""docstring for Element"""
	def __init__(self,index : int = 0,nom : str = "",red : int = 0 ,blue : int = 0,green : int = 0) -> None:
		self.index = index
		self.nom = nom 
		self.color = [red,blue,green]

	@classmethod
	def byBdd(cls,index):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute("SELECT * FROM Element where id = ?",(index,))

		result = res.fetchone()

		return Element(result[0],result[1],result[2],result[3],result[4])

	def __str__(self):
		return f"id : "+str(self.index)+ " nom : "+str(self.nom)+ " color : "+str(self.color)