from Item import *

class Lieu(object):
	"""docstring pour un Lieu
	Un lieu est lié a un channel et permet de créer d'autre lieu et le channel ave
	"""
	def __init__(self, channel,description : str, isMonster : bool):
		self.channel = channel #channel discord
		self.description = description # description lieu 
		self.isMonster = isMonster # si le lieu a des monstres ou pas
		self.objects = []

	#gere ici si un joueur peut aller a un lieu ou pas, gere le channel 
	def autorize(self,character):
		pass

	#gere ici si un joeur ne peut pas aller a un lieu ou pas, gere le channel
	def inautorize(self,character):
		pass

	#envoie un message via le channel
	async def sendMessage(self,message : str):
		await self.channel.send(message)
