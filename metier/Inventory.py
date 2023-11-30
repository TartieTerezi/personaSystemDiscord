from Item import *

class Inventory(object):
	"""docstring for Inventary"""
	def __init__(self) -> None:
		self.data : dict = {}

	def in_inventory(self,_item : Item) -> bool:
		"""Retourne Vrai ou Faux si un item se trouve dans l'inventaire du joueur."""
		return (_item not in self.data.keys())
	
	def deleteItem(self) -> None:
		"""Supprime les items dont le joueur n'as plus en stock."""
		itemsToDelete : list[Item] = []

		for item in self.data:
			if(self.data[item] == 0):
				itemsToDelete.append(item)

		for item in itemsToDelete:
			self.data.pop(item)

	def useItem(self,_item : Item) -> bool:
		""""Utilise un item et renvoie si l'item a ete utilise."""
		#si l'item n'est pas utilisable
		if(_item.is_useable() == False):
			return False

		#verifie le nombre d'objets disponible
		if(self.remove_item(_item)):
			_item.use(self)
		else:
			return False

	def add_item(self,_item : Item,_amount : int = 1) -> None:
		"""Ajoute un Item dans l'inventaire."""
		if self.in_inventory(_item):
			self.data[_item] = _amount
		else:
			self.data[_item] += _amount

	def get_item(self,_item : Item) -> int:
		"""Recupere le nombre d'item dans l'inventaire."""
		return self.data[_item]

	def getItemByName(self,_nameItem : str) -> Item:
		"""Recupere l'item selon son nom."""
		for item in self.data:
			if(item.nom == _nameItem):
				return item

	def remove_item(self,item,amount=1) -> bool:
		"""Renvoie true si l'item a ete enleve, renvoir False sinon"""
		#seulement si un item est déjà présent
		if(self.in_inventory(item)):
			return False

		#regarde si il y aassez d'item dans l'inventaire
		if(self.data[item]-amount>=0):
			self.data[item] -= amount
			return True
		else:
			return False