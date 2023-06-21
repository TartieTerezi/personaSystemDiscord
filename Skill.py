from Element import Element

class Skill(object):
	"""docstring for Skill"""
	def __init__(self,nom : str,element : Element,description : str,cout : int,puissance : int,precision : int,isHealing : bool):
		self.nom = nom
		self.element = element
		self.description = description
		self.cout = cout
		self.puissance = puissance
		self.precision = precision
		self.isHealing = isHealing

	def __str__(self):
		return f"Skill(nom={self.nom},Element={self.element},description={self.description},cout={self.cout},puissance={self.puissance},precision={self.precision},isHealing={self.isHealing})"

	def getCount(self):
		typeDeCout = ""

		typeDeCout += str(self.cout)
		
		if(self.element == Element.PHYSIQUE):
			typeDeCout += "% pv"
		else:
			typeDeCout += " pc"

		return typeDeCout