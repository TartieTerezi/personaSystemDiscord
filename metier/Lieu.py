class Lieu(object):
	"""docstring for Lieu
	Un lieu est lié a un channel et permet de créer d'autre lieu et le channel ave
	"""
	def __init__(self, channel,description : str, isMonster : bool):
		self.channel = channel #channel discord
		self.description = description # description lieu 
		self.isMonster = isMonster # si le lieu a des monstres ou pas
	
	#gere ici si un joueur peut aller a un lieu ou pas, gere le channel 
	def autorize(self,character):
		pass

	#gere ici si un joeur ne peut pas aller a un lieu ou pas, gere le channel
	def inautorize(self,character):
		pass

