
class Mechanism(object):
	"""docstring for Switch"""
	def __init__(self,index : int,nom : str,isActive : bool = False,info : str = ""):
		self.id = index #id du mechanism
		self.nom = nom #nom du mechanism
		self.info = info #info du mechanism
		self.isActive = isActive

	def __str__(self):
		return f"(id={self.id},nom={self.nom},info={self.info})"