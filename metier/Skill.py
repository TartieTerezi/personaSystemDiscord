from Element import Element
import sqlite3

class Skill(object):
	"""docstring for Skill"""
	def __init__(self,index : int = 0,nom : str = "",idElement : int = 0,description : str = "",cout : int = 0,puissance : int = 0,precision : int = 0):
		self.index = index
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.description = description
		self.cout = cout
		self.puissance = puissance
		self.precision = precision

	def __str__(self):
		return f"Skill(nom={self.nom},Element={self.element},description={self.description},cout={self.cout},puissance={self.puissance},precision={self.precision},isHealing={self.isHealing})"

	@classmethod
	def byBdd(cls,index : int):
		con = sqlite3.connect("bdd/persona.db")
		cur = con.cursor()

		res = cur.execute("SELECT * FROM Skill where id = ?",(index,))

		result = res.fetchone()

		return Skill(result[0],result[1],result[2],result[3],result[4],result[5],result[6])

	#effet du skill ici un effet d'attaque sur une cible unique
	def effect(self,persona):

		pass

	def getCount(self):
		typeDeCout = ""

		typeDeCout += str(self.cout)
		
		if(self.element.index == 1):
			typeDeCout += "% pv"
		else:
			typeDeCout += " pc"

		return typeDeCout