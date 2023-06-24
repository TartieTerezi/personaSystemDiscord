

class Item(object):
	"""docstring for Item"""
	def __init__(self,index : int,nom : str,info : str = ""):
		self.id = index
		self.nom = nom
		self.info = info

	def use(self,character):
		pass

	def is_useable(self):
		return False

	def is_equipeable(self):
		return False

	def equip(self,character):
		pass

	def __str__(self):
		return f"(id={self.id},nom={self.nom},info={self.info})"


class Weapon(Item):
	"""docstring for Weapon"""
	def __init__(self,index : int,nom : str,puissance : int, precision : int,info : str = ""):
		Item.__init__(self,index,nom)
		self.puissance = puissance
		self.precision = precision

	def is_equipeable(self):
		return True

	def equip(self,character):
		character.arme = self
		character.remove_item(self)

	def __str__(self):
		return f"(id={self.id},nom={self.nom},power={self.puissance},precision={self.precision},info={self.info})"




from Character import Character