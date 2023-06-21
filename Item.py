

class Item(object):
	"""docstring for Item"""
	def __init__(self,index : int,nom : str):
		self.id = index
		self.nom = nom

	def __str__(self):
		return f"(id={self.id},nom={self.nom}"
