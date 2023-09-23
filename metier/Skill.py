from Element import Element

class Skill(object):
	"""docstring for Skill"""
	def __init__(self,nom : str,idElement : int,description : str,cout : int,puissance : int,precision : int):
		self.nom = nom
		self.element = Element.byBdd(idElement)
		self.description = description
		self.cout = cout
		self.puissance = puissance
		self.precision = precision

	def __str__(self):
		return f"Skill(nom={self.nom},Element={self.element},description={self.description},cout={self.cout},puissance={self.puissance},precision={self.precision},isHealing={self.isHealing})"


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