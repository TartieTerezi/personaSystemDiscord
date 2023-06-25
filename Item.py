

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
		Item.__init__(self,index,nom,info)
		self.puissance = puissance
		self.precision = precision

	def is_equipeable(self):
		return True

	def equip(self,character):
		character.arme = self
		character.remove_item(self)

	def __str__(self):
		return f"(id={self.id},nom={self.nom},power={self.puissance},precision={self.precision},info={self.info})"


class HealingObject(Item):
	"""docstring for healing object"""
	def __init__(self,index : int,nom : str,pvHeal : int,pcHeal : int,isPercent : int = False,info : str = ""):
		Item.__init__(self,index,nom,info)
		self.pvHeal = pvHeal
		self.pcHeal = pcHeal
		self.isPercent = isPercent

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
		

from Character import Character