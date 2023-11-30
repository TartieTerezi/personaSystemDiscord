
class Item(object):
	"""
		Un Item la base de tout les Items du rp. 
	"""
	def __init__(self,index : int,nom : str,info : str = ""):
		self.id : int = index  
		""" Index de l'item dans la bdd. """
		self.nom : str = nom 
		""" Nom de l'item. """
		self.info : str = info 
		""" Information sur l'Item. """

	def is_useable(self) -> bool:
		"""
			Retourne un boolean Vrai ou Faux selon si l'objet peut etre utilise.
		"""
		return False

	def is_equipeable(self) -> bool:
		"""
			Retourne un boolean Vrai ou Faux selon si l'objet peut etre equipe.
		"""
		return False

	def equip(self,character) -> None:
		"""
			Equipe l'objet a un personnage de type Character.
		"""
		pass

	def use(self,character) -> None:
		"""
			utilise l'objet sur un personnage de type Character.
		"""
		pass

	def __str__(self) -> str:
		return f"(id={self.id},nom={self.nom},info={self.info})"

class Weapon(Item):
	"""
		Arme pouvant etre equipe par des personnage, inclue une precision et une puissance d'attaque
	"""
	def __init__(self,index : int,nom : str,puissance : int, precision : int,info : str = ""):
		Item.__init__(self,index,nom,info)
		self.puissance : int = puissance
		""" Puissance de l'arme. """
		self.precision = precision
		"""" Precision de l'arme. """

	def is_equipeable(self):
		return True

	def equip(self,character):
		character.arme = self
		character.inventaire.remove_item(self)

	def __str__(self):
		return f"(id={self.id},nom={self.nom},power={self.puissance},precision={self.precision},info={self.info})"

class HealingObject(Item):
	"""
		Objet pouvant soigner les pv et / ou les pc
	"""
	def __init__(self,index : int,nom : str,pvHeal : int,pcHeal : int,isPercent : int = False,info : str = ""):
		Item.__init__(self,index,nom,info)
		self.pvHeal : int = pvHeal
		""" Puissance de soin des pv. """
		self.pcHeal = pcHeal
		""" Puissance de soin des pc. """
		self.isPercent : bool = isPercent
		""" Determine si le soin est affecte en pourcentage ou de facon statique. """

	def use(self,character):
		if(self.isPercent):
			character.pv += int(character.maxPv / 100 * self.pvHeal)
			character.pc += int(character.maxPc / 100 * self.pcHeal)
		else:
			character.pv += self.pvHeal
			character.pc += self.pcHeal 
		
		if (character.pc > character.maxPc):
			character.pc = character.maxPc
		
		if (character.pv > character.maxPv):
			character.pv = character.maxPv

	def is_useable(self):
		return True

	def __str__(self):
		heal = ""

		if self.pvHeal!=0:
			heal += str(self.pvHeal)
			if(self.isPercent):
				heal += "%"
			heal += "pv "

		if self.pcHeal!=0:
			heal += str(self.pcHeal)
			if(self.isPercent):
				heal += "%"
			heal += "pc "		


		return f"(id={self.id},nom={self.nom},info={self.info},heal={heal})"
		
from Character import *