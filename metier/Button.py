from Mechanism import Mechanism

class Button(object):
	"""docstring for Switch"""
	def __init__(self,index : int,nom : str,isActive : bool = False,info : str = "",mechanism = []):
		self.id = index #id du bouton
		self.nom = nom #nom du bouton
		self.info = info #info du bouton
		self.mechanismLink = mechanism #mecanisme lié a activer
		self.isActive = isActive

	def use(self):
		self.isActive = not self.isActive

		print(self.isActive)

		for mechanism in self.mechanismLink:
			mechanism.isActive = self.isActive


	def __str__(self):
		return f"(id={self.id},nom={self.nom},info={self.info})"